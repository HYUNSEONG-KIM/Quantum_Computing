
from __future__ import annotations

VERSION = "0.0.1"

# Standard modules
from typing import *
from collections import OrderedDict
from itertools import combinations, combinations_with_replacement as re_combi, product
from functools import reduce
from pathlib import Path

from sys import float_info
FLOAT_EPS = 1E4 * float_info.min
float_tol = 1E-8


# Dependenct modules
import numpy as np
from scipy import linalg
import pandas as pd



I = np.eye(2)
pauli_X = np.array([[0, 1], [1, 0]], dtype=complex)
pauli_Y = complex(0, 1)*np.array([[0, -1], [1, 0]], dtype=complex)
pauli_Z = np.array([[1, 0], [0, -1]], dtype=complex)
p_basis = {"I":I, "X":pauli_X, "Y":pauli_Y, "Z":pauli_Z}




class Hamiltonian:
    def __init__(self, 
                 H:np.matrix, 
                 tols=(1E4*float_tol , float_tol), 
                 pauli_basis:Union[None, dict]=None):
        assert len(H.shape) ==2, f"H must be 2dim matrix. current: {H.shape}."
        n1, n2 = H.shape
        assert n1 == n2, f"Hamiltonian must be square matrix. Current:{(n1, n2)}."
        assert np.allclose(H, H.H, *tols), f"Hamiltonian must be a hermite matrix. Relative, absolute tolerance, {tols}."
        assert bin(8)[2:].count("1") == 1, f"Dimension must be a 2^n. Current:{n1}."
        
        self.Hamiltonian = H
        
        # None or Dataframe
        self.local_decomposition = self._check_decomposition(pauli_basis)  
        self.exist_decompositon = False if pauli_basis is None else True 
        self.x_family = None # save as integer 2dim matrix point the latin matrix.
        self.z_family = None
        self.coefficients = None # Latin matrix corresponding coefficient.
        
        self.qubit_num = len(bin(H.shape[0])[3:]) # Consider a 1 bit position of 2^n integer.
    # Basic utils
    @staticmethod
    def pstr_to_matrix(pstr):
        result = []
        for p in pstr:
            result.append(p_basis[p])
        return krons(result)
    @staticmethod
    def pstr_to_xz_fam_code(pstr:str)->Tuple[int, int]:
        num = 1
        x_num = 0 # Consider a bit represenation
        z_num = 0

        p_map = {"I":(0,0), "X":(1, 0), "Y":(1,1), "Z":(0,1)}
        for p in reversed(pstr):
            nx, nz = p_map[p]
            x_num += nx*num
            z_num += nz*num
            num += num
        return x_num, z_num
    @staticmethod
    def xz_fam_code_to_pstr(ns:Tuple[int, int], l:int):
        assert l>0, "l must be positive integer and greater than 0."
        nx, nz = ns
        max_int_1 = 2**l
        assert (nx < max_int_1 and nz < max_int_1), "The given integers and the qubit dim are not matched."
        if nx==0:
            st = format(nz, f"0{l}b")
            st = st.replace("0", "I")
            st = st.replace("1", "Z")
            return st
        if nz==0:
            st = format(nx, f"0{l}b")
            st = st.replace("0", "I")
            st = st.replace("1", "X")
            return st
        
        st_x = format(nx, f"0{l}b")
        st_z = format(nz, f"0{l}b")

        result = []
        for x, z in zip(st_x, st_z):
            if x == z:
                if x =="1":
                    result.append("Y")
                else: 
                    result.append("I")
            elif x > z:
                result.append("X")
            else:
                result.append("Z")
        return "".join(result)

    @staticmethod
    def p_poly_to_H(p_poly:dict):
        """Convert pauli-polynomial of dictionary form to total Hamiltonian matrix.
        The given polynomial must be a dictionary whose keys are pauli-terms and the values are coefficient.

        Args:
            pstrs (dict): _description_
        """
        n = len(list(p_poly.keys())[0])
        dim = int(2**n)
        shape = (dim, dim)
        result = np.zeros(shape, dtype=complex)
        for pstr in p_poly:
            coef = p_poly[pstr]
            result += coef*Hamiltonian.pstr_to_matrix(pstr)
        return result
    @staticmethod
    def H_to_p_poly(H, tol=float_tol, include_zeros=False):
        n = len(bin(H.shape[0])[3:])
        p_mat, p_str = Hamiltonian.generate_pauli_terms(n)
        poly = {}
        for p_m, p_str in zip(p_mat, p_str):
            coef = frobenius_inner(p_m, H)
            coef = 0 if np.absolute(coef) < tol else coef
            if include_zeros:
                poly[p_str] = coef
            elif coef != 0:
                poly[p_str] = coef
        return poly
    @staticmethod
    def p_poly_to_latin(p_poly:dict, full=False):
        pass
    @staticmethod
    def generate_pauli_terms(
        qubit_num:int, 
        only:Literal["both", "string", "matrix"]="both")-> Union[Tuple[Iterable, Iterable], Iterable]:
        """Generate full set of pauli-terms in matrix and strings of `n` number of qubit system.

        Args:
            qubit_num (int): _description_
            only (Literal[&quot;both&quot;, &quot;string&quot;, &quot;matrix&quot;], optional): _description_. Defaults to "both".

        Returns:
            _type_: _description_
        """
        n = int(qubit_num)
        assert n >0, "The given argument must be a positive natural number."
        
        p_xs =  Hamiltonian.get_pauli_family_matrix(n, fam="X")
        p_zs =  Hamiltonian.get_pauli_family_matrix(n, fam="Z")
        p_xs_str = Hamiltonian.get_pauli_family_string(n, fam="X")
        p_zs_str = Hamiltonian.get_pauli_family_string(n, fam="Z")

        result = []
        if only=="both" or only=="matrix":
            p_g = []
            p_g_str =[]
            for x_i, x_str in zip(p_xs, p_xs_str):
                for z_j, z_str in zip(p_zs, p_zs_str):
                    g = x_i@z_j

                    g_coef, g_str = get_coef(x_str, z_str)

                    p_g.append(g_coef*g)
                    p_g_str.append(g_str)
            result.append(p_g) 
            if only =="both":
                result.append(p_g_str)
        elif only=="string":
            p_g_str = []
            for x_str in p_xs_str:
                for z_str in p_zs_str:
                    p_g_str.append(g_str)
            result.append(p_g_str)
        return result
    @staticmethod
    def get_pauli_family_string(n, fam="Z"):
        return list(map(lambda x: "".join(x), product(f"I{fam}", repeat=int(n))))
    @staticmethod
    def get_pauli_family_matrix(n:int, fam="Z")->Iterable[np.matrix]:
        """Get pauli_family of `n` qubits of `fam` family. 

        Args:
            n (int): Number of qubits. The output matrices are :math:`2^n`.
            fam (str, optional): Type of Pauli-family of X, Y, or Z. Defaults to "Z".

        Returns:
            Iterable[np.matrix]: list of Pauli-matrices
        """
        G = pauli_Z if fam=="Z" else (pauli_X if fam=="X" else pauli_Y)

        return list(map(krons, product([I, G], repeat=int(n))))
        
    #--------------------------------------------------------------
    def _check_decomposition(self, pauli_basis):
        if pauli_basis is None:
            return None
        pass    
    def get_decomposition(self, H:np.matrix, tol=float_tol ):
        pass
    def decompose(self, tol=float_tol , replace = False):
        if self.exist_decompositon:
            if not replace:
                return self.local_decomposition
        
        if replace:
            self.local_decomposition = self.get_decomposition(self.H, tol) 
            self.exist_decompositon = True
            return self.local_decomposition
        return self.get_decomposition(self.H, tol) 
    def save_as(self, filepath:Union[Path, str]):
        if isinstance(filepath, str):
            filepath = Path(filepath)
            
        pass
    #--------------------------------------------------------------
    @property
    def pauli_decomposition(self):
        if self.exist_decompositon:
            pass
        return None
    @property
    def xz_family(self):
        if self.exist_decompositon:
            pass
        return None
    @property
    def latin_matrix(self):
        if self.exist_decompositon:
            pass
        return None    
    #--------------------------------------------------------------
    @classmethod
    def from_latin_matrix(cls:Hamiltonian, 
                      l_matrix:np.matrix, 
                      coefficient:Union[np.matrix, None]=None)->Hamiltonian:
        pass
    @classmethod
    def from_pauli_polynomial(cls:Hamiltonian, 
                               p_poly:Union[dict, np.ndarray], 
                               p_coef:Union[None, np.ndarray]=None)-> Hamiltonian:
        pass
    @classmethod
    def from_data(cls:Hamiltonian, file_path)->Hamiltonian:
        pass
    #------------------------------
    