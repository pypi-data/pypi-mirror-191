# -*- coding: utf-8 -*-
import os
from typing import List

import numpy as np
import path
import torch
from ase import Atoms
from ase.calculators.calculator import Calculator, PropertyNotImplementedError

from hpc2ml.data.structuretodata import StructureToData
from hpc2ml.nn.flow_geo import simple_predict
from hpc2ml.nn.metrics import mlm


class GNNEICalculater(Calculator):
    implemented_properties: List[str] = ["energy", "forces"]

    _deprecated = object()

    'Properties calculator can handle (energy, forces)'

    def __init__(self, model, resume_file, atoms=None, directory='.', convert=StructureToData(),
                 properties=None,
                 device="cpu",
                 **kwargs):
        """Basic calculator implementation.

        restart: str
            Prefix for restart file.  May contain a directory. Default
            is None: don't restart.

        directory: str or PurePath
            Working directory in which to read and write files and
            perform calculations.
        label: str
            Name used for all files.  Not supported by all calculators.
            May contain a directory, but please use the directory parameter
            for that instead.
        atoms: Atoms object
            Optional Atoms object to which the calculator will be
            attached.  When restarting, atoms will get its positions and
            unit-cell updated from file.
        """
        super(GNNEICalculater, self).__init__(atoms, directory=directory, **kwargs)

        self.model = model
        self.convert = convert
        self.convert.tq = False
        self.resume_file = resume_file
        self.device = torch.device(device)
        if properties is not None:
            self.implemented_properties=properties

        from hpc2ml.nn.flow_geo import load_check_point

        resume_file = path.Path(self.directory) / self.resume_file

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        model, optimizer, start_epoch, best_error, note = load_check_point(self.model,
                                                                           resume_file=resume_file,
                                                                           optimizer=optimizer,
                                                                           device=self.device)
        # temp/ delete it later
        note1 = {}
        if "mean" in note:
            if "energy" in note1:
                note1["energy"].update({"mean":note["mean"]})
            else:
                note1["energy"] = {"mean": note["mean"]}

        if "std" in note:
            if "energy" in note1:
                note1["energy"].update({"std":note["std"]})
            else:
                note1["energy"] = {"std": note["std"]}

        if "mean1" in note:
            if "forces" in note1:
                note1["forces"].update({"mean":note["mean1"]})
            else:
                note1["forces"] = {"mean": note["mean1"]}

        if "std1" in note:
            if "forces" in note1:
                note1["forces"].update({"std":note["std1"]})
            else:
                note1["forces"] = {"std": note["std1"]}
        note =note1
        #####

        self.model = model
        self.optimizer = optimizer
        self.note = note
        self.start_epoch = start_epoch
        self.best_error = best_error

    def train(self, atoms, batch_data=None, **kwargs):
        """train"""
        print("Re-train model...")

        from torch_geometric.loader import DataLoader
        from hpc2ml.nn.flow_geo import LearningFlow

        if batch_data is None:
            dataset = self.get_bath_data(atoms, **kwargs)
        else:
            dataset = batch_data

        test_loader = DataLoader(dataset, batch_size=32, shuffle=False)

        train_loader = DataLoader(dataset, batch_size=32, shuffle=False)
        # # LearningFlow
        print_what =""
        self.lf = LearningFlow(self.model, train_loader, test_loader=test_loader,
                               loss_method=mlm, optimizer=self.optimizer,
                               device=self.device, note=self.note, multi_loss=True,
                               target_name=tuple(self.implemented_properties),
                               checkpoint=True, store_filename=self.resume_file,
                               loss_threshold=0.003,print_what=print_what,
                               )

        self.lf.start_epoch = self.start_epoch
        self.lf.best_error = self.best_error
        self.lf.run(epoch=3)
        print("Done.")

    def get_bath_data(self, atoms=None, **kwargs):

        from hpc2ml.data.batchdata import MtBatchData

        dataset = MtBatchData.from_atoms(atoms, **kwargs, convert=self.convert)
        dataset.scale(dct=self.note)
        return dataset

    def get_property(self, name, atoms=None, allow_calculation=True):
        if name not in self.implemented_properties:
            raise PropertyNotImplementedError('{} property not implemented'
                                              .format(name))

        if atoms is None:
            atoms = self.atoms
        else:
            system_changes = self.check_state(atoms)
            if system_changes:
                self.reset()
        if name not in self.results:
            if not allow_calculation:
                return None
            self.calculate(atoms)

        if name not in self.results:
            # For some reason the calculator was not able to do what we want,
            # and that is OK.
            raise PropertyNotImplementedError('{} not present in this '
                                              'calculation'.format(name))

        result = self.results[name]
        if isinstance(result, np.ndarray):
            result = result.copy()
        return result

    def calculate(self, atoms=None, batch_data=None):
        properties = tuple(self.implemented_properties)

        if atoms is not None:
            self.atoms = atoms.copy()

        if not os.path.isdir(self._directory):
            os.makedirs(self._directory)

        from torch_geometric.loader import DataLoader

        if batch_data is None:
            dataset = self.get_bath_data(atoms)
        else:
            dataset = batch_data

        predict_loader = DataLoader(dataset, batch_size=32, shuffle=False)

        res = simple_predict(self.model, predict_loader, return_y_true=False, device=self.device,
                             process_out=None, process_label=None, target_name=properties,
                             multi_loss=True)

        for k, v in zip(properties, res):
            if isinstance(v, torch.Tensor):
                v = v.detach().cpu().numpy()
            if hasattr(v, "shape") and sum(v.shape) <= 2:
                v = v[0]
            if hasattr(v, "shape") and len(v.shape) == 1:
                v = v.reshape(1, -1)
            self.results.update({k: v})

        if "stress" not in properties:
            self.results["stress"] = np.zeros((3, 3))

    def calculate_batch(self, atoms, batch_data=None):
        properties = tuple(self.implemented_properties)
        results_batch = {}

        if isinstance(atoms, Atoms):
            atoms = [atoms, ]
        else:
            atoms = atoms

        if not os.path.isdir(self._directory):
            os.makedirs(self._directory)

        from torch_geometric.loader import DataLoader

        if batch_data is None:
            dataset = self.get_bath_data(atoms)
        else:
            dataset = batch_data

        l = len(atoms)

        predict_loader = DataLoader(dataset, batch_size=32, shuffle=False)

        res = simple_predict(self.model, predict_loader, return_y_true=False, device=self.device,
                             process_out=None, process_label=None, target_name=properties,
                             multi_loss=True)

        for k, v in zip(properties, res):
            if isinstance(v, torch.Tensor):
                v = v.detach().cpu().numpy()
            if k in ["forces", "stress"]:
                v = v.reshape(l, -1)
            results_batch.update({k: v})

        if "stress" not in properties:
            results_batch["stress"] = np.zeros((l, 9), dtype=np.float32)
        return results_batch


class GNNMultiEICalculater(Calculator):
    implemented_properties: List[str] = ["energy", "forces"]

    _deprecated = object()

    'Properties calculator can handle (energy, forces)'

    def __init__(self, models, resume_files: List, atoms=None, directory='.', convert=StructureToData(),
                 device="cpu", properties=None,
                 **kwargs):
        if properties is not None:
            self.implemented_properties = properties

        self.num = len(resume_files)

        if not isinstance(models, List):
            models = [models for _ in range(self.num)]

        if isinstance(models, List):
            assert len(models) == len(resume_files)

        self.resume_files = [path.Path(directory) / i for i in resume_files]

        self.sub = []
        for mi, ri in zip(models, self.resume_files):
            single = GNNEICalculater(mi, ri, atoms=atoms, directory=directory,
                                     properties=self.implemented_properties,
                                     convert=convert, device=device, **kwargs)

            self.sub.append(single)

        self.note = self.sub[0].note  # keep it is the same
        self.convert = convert
        super(GNNMultiEICalculater, self).__init__(atoms, directory=directory, **kwargs)

    def get_bath_data(self, atoms=None, **kwargs):

        from hpc2ml.data.batchdata import MtBatchData
        dataset = MtBatchData.from_atoms(atoms, **kwargs, convert=self.convert)
        dataset.scale(dct=self.note)
        return dataset

    def get_property(self, name, atoms=None, allow_calculation=True):
        if name not in self.implemented_properties:
            raise PropertyNotImplementedError('{} property not implemented'
                                              .format(name))

        if atoms is None:
            atoms = self.atoms
        else:
            system_changes = self.check_state(atoms)
            if system_changes:
                self.reset()
        if name not in self.results:
            if not allow_calculation:
                return None
            self.calculate(atoms)

        if name not in self.results:
            # For some reason the calculator was not able to do what we want,
            # and that is OK.
            raise PropertyNotImplementedError('{} not present in this '
                                              'calculation'.format(name))

        result = self.results[name]
        if isinstance(result, np.ndarray):
            result = result.copy()
        return result

    def train(self, atoms=None, **kwargs):
        """train"""

        dataset = self.get_bath_data(atoms=self.atoms, **kwargs)

        for si in self.sub:
            si.train(atoms=atoms, batch_data=dataset)

    def calculate(self, atoms=None, properties=None):
        if properties is None:
            properties = tuple(self.implemented_properties)
        self.results = {}

        if atoms is not None:
            self.atoms = atoms.copy()

        dataset = self.get_bath_data(atoms=atoms)

        for si in self.sub:
            si.calculate(atoms=atoms, batch_data=dataset)

            for pi in properties:
                if f"{pi}_all" in self.results:
                    self.results[f"{pi}_all"].append(si.results[pi])

                else:
                    self.results[f"{pi}_all"] = [si.results[pi]]
        for pi in properties:
            piv = np.array(self.results[f"{pi}_all"])
            if piv.ndim > 1:
                self.results[f"{pi}"] = np.mean(piv, axis=0)
                self.results[f"{pi}_std"] = np.std(piv, axis=0)
            else:
                self.results[f"{pi}"] = np.mean(piv)
                self.results[f"{pi}_std"] = np.std(piv)

    def calculate_batch(self, atoms, properties=None):
        if properties is None:
            properties = tuple(self.implemented_properties)
        self.results = {}

        if isinstance(atoms, Atoms):
            atoms = [atoms, ]
        else:
            atoms = atoms

        dataset = self.get_bath_data(atoms=atoms)

        result_batch = {}

        for si in self.sub:
            res = si.calculate_batch(atoms=atoms, batch_data=dataset)

            for pi in properties:
                if f"{pi}_all" in res:
                    result_batch[f"{pi}_all"].append(res[pi])

                else:
                    result_batch[f"{pi}_all"] = [res[pi]]
        for pi in properties:
            piv = np.array(result_batch[f"{pi}_all"])
            if piv.ndim > 1:
                result_batch[f"{pi}"] = np.mean(piv, axis=0)
                result_batch[f"{pi}_std"] = np.std(piv, axis=0)
            else:
                result_batch[f"{pi}"] = np.mean(piv)
                result_batch[f"{pi}_std"] = np.std(piv)
        return result_batch