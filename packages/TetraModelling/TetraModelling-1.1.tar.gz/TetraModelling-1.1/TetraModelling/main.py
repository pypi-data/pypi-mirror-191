"""
Imported a Custom created class Polyhedron
Import Numpy for handling arrays
"""

import os
import numpy as np
import alphashape
import trimesh
from itertools import combinations
from pathlib import Path
import shutil
import math

from chimerax.core.models import Model
from chimerax.core.commands import run
from chimerax.graphics import Drawing
from chimerax.model_panel import tool

# colors to use
magenta = (255, 0, 255, 255)
cyan = (0, 255, 255, 255)
gold = (255, 215, 0, 255)
bright_green = (70, 255, 0, 255)
navy_blue = (0, 30, 128, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)
white = (255, 255, 255, 255)
colors = [magenta, white]

# Constants
ht3 = 0.81649658092772603273242802490196379732198249355222337614423086
ht2 = 0.86602540378443864676372317075293618347140262690519031402790349


class Tetra:

    def __init__(self, session):
        self.chain_ids = None
        self.model_ids = None
        self.all_points = None
        self.session = session
        self.model_list = None
        self.t = Drawing('tetrahedrons')
        self.va = []
        self.ta = []
        self.massing_vertices = []
        self.avg_edge_length = 0

        self.model_list = self.session.models.list()
        for model in self.model_list:
            try:
                model.chains
            except AttributeError:
                self.model_list.remove(model)

    def avg_length(self):
        count = 0
        for model in self.model_list:
            if model.name not in self.model_ids:
                continue
            for chain in model.chains:
                if chain.chain_id not in self.chain_ids[model.name]:
                    continue
                for amino_index in range(len(chain.residues)):
                    if chain.residues[amino_index] is None:
                        continue
                    residue = chain.residues[amino_index].atoms
                    if 'CA' != residue.names[1]:
                        continue
                    mid_N_point = residue[0].coord
                    mid_CO_point = residue[2].coord
                    if amino_index != 0 and chain.residues[amino_index - 1] is not None:
                        mid_N_point = (mid_N_point + chain.residues[amino_index - 1].atoms[2].coord) * 0.5
                    if amino_index != len(chain.residues) - 1 and chain.residues[amino_index + 1] is not None:
                        mid_CO_point = (mid_CO_point + chain.residues[amino_index + 1].atoms[0].coord) * 0.5
                    e = np.linalg.norm(mid_N_point - mid_CO_point)
                    self.avg_edge_length += e
                    count += 1
            self.avg_edge_length /= count

    def provide_model(self, regular=False):
        amino_count = 0
        amino_skipped_count = 0
        c_alpha_vertex = []
        all_original_vertex = []
        original_c_alpha_vertex = []

        for model in self.model_list:
            if model.name not in self.model_ids:
                continue
            for chain in model.chains:
                if chain.chain_id not in self.chain_ids[model.name]:
                    continue
                prev_co_cord = None
                for amino_index in range(len(chain.residues)):
                    if chain.residues[amino_index] is None:
                        continue
                    vertex_points = []
                    residue = chain.residues[amino_index].atoms
                    n_cord = residue[0].coord
                    co_cord = residue[2].coord
                    if amino_index != 0 and chain.residues[amino_index - 1] is not None:
                        if regular and prev_co_cord is not None:
                            n_cord = prev_co_cord
                        else:
                            n_cord = (n_cord + chain.residues[amino_index - 1].atoms[2].coord) * 0.5
                    if amino_index != len(chain.residues) - 1 and chain.residues[amino_index + 1] is not None:
                        co_cord = (co_cord + chain.residues[amino_index + 1].atoms[0].coord) * 0.5
                    co_n = n_cord - co_cord
                    norm_co_n = np.linalg.norm(co_n)
                    c_beta_coord = None
                    c_alpha_cord = None
                    if regular:
                        co_n_dir = co_n / norm_co_n
                        co_n = co_n_dir * self.avg_edge_length
                        co_cord = n_cord - co_n
                        norm_co_n = self.avg_edge_length
                        prev_co_cord = co_cord
                    if 'CA' != residue.names[1]:
                        prev_co_cord = None
                        continue
                    if len(residue) == 4:
                        c_alpha_cord = residue[1].coord
                        mid_vec = n_cord - co_cord
                        mid_point_vector = np.array([-1 / mid_vec[0], 1 / mid_vec[1], 0])
                    elif len(residue) > 4:
                        c_beta_coord = residue[4].coord
                        c_alpha_cord = residue[1].coord
                        co_c_beta = c_beta_coord - co_cord
                        norm_co_c_beta = np.linalg.norm(co_c_beta)
                        move_to_mid_line = (0.5 * norm_co_n - (np.dot(co_n, co_c_beta) / norm_co_n)) * (co_n / norm_co_n)
                        mid_point_vector = c_beta_coord + move_to_mid_line - (co_cord + n_cord) * 0.5
                    mid_point_vector *= ht2 * norm_co_n / np.linalg.norm(mid_point_vector)
                    c_beta_coord = (co_cord + n_cord) * 0.5 + mid_point_vector
                    centroid = (c_beta_coord + co_cord + n_cord) / 3
                    direction = np.cross((c_beta_coord - co_cord), (n_cord - co_cord))
                    unit_dir = direction / np.linalg.norm(direction)
                    vec = c_alpha_cord - centroid
                    cos_theta = np.dot(unit_dir, vec) / np.linalg.norm(vec)
                    if cos_theta < 0:
                        unit_dir *= -1
                    H_vector = ht3 * norm_co_n * unit_dir
                    h_cord = centroid + H_vector
                    norm_c_beta_n = np.linalg.norm(c_beta_coord - n_cord)
                    norm_co_c_beta = np.linalg.norm(co_cord - c_beta_coord)
                    norm_co_h = np.linalg.norm(co_cord - h_cord)
                    norm_c_beta_h = np.linalg.norm(c_beta_coord - h_cord)
                    norm_n_h = np.linalg.norm(n_cord - h_cord)
                    if len(residue) == 4:
                        original_cb = c_beta_coord
                    else:
                        original_cb = residue[4].coord
                    vertices = [n_cord, co_cord, c_beta_coord, h_cord]
                    original_vertices = np.array([residue[0].coord, residue[2].coord, original_cb, vertices[-1]])
                    edges = np.array([norm_co_n, norm_c_beta_n, norm_co_c_beta, norm_co_h, norm_c_beta_h, norm_n_h])
                    original_edges = np.array([np.linalg.norm(original_vertices[0] - original_vertices[1]),
                                               np.linalg.norm(original_vertices[0] - original_vertices[2]),
                                               np.linalg.norm(original_vertices[1] - original_vertices[2]),
                                               np.linalg.norm(original_vertices[1] - original_vertices[3]),
                                               np.linalg.norm(original_vertices[2] - original_vertices[3]),
                                               np.linalg.norm(original_vertices[0] - original_vertices[3])])
                    face_index = list(combinations(np.arange(amino_count * 4, (amino_count + 1) * 4), 3))
                    self.va.append(vertices)
                    self.ta.extend(face_index)
                    c_alpha_vertex.append(c_alpha_cord)
                    all_original_vertex.extend(original_vertices)
                    original_c_alpha_vertex.append((n_cord + co_cord + c_beta_coord + h_cord) / 4)
                    amino_count += 1

        self.va = np.array(self.va, np.float32)
        self.ta = np.array(self.ta, np.int32)

    def tetrahedron_model(self, pdb_name='1dn3', model_ids=None, chain_ids=None, reg=True, seq=False):
        self.model_ids = model_ids
        self.chain_ids = chain_ids
        if self.chain_ids is None:
            chains = []
            for model in self.model_list:
                chains.append([i.chain_id for i in model.chains])
            self.chain_ids = {model.name: chain_id for (model, chain_id) in zip(self.model_list, chains)}
        if self.model_ids is None:
            self.model_ids = [model.name for model in self.model_list]

        self.avg_length()
        self.provide_model(reg)

        if seq:
            if seq[2] + 1 < len(self.va):
                seq[2] += 2
            elif seq[2] + 1 == len(self.va):
                seq[2] += 1

            va = np.reshape(np.concatenate((self.va[:seq[1]], self.va[seq[2]:])),
                            ((self.va.shape[0] - seq[2] + seq[1]) * self.va.shape[1], self.va.shape[2]))
            self.ta = self.ta[:-(seq[2] - seq[1])*4]
        else:
            va = np.reshape(self.va, (self.va.shape[0] * self.va.shape[1], self.va.shape[2]))

        self.t.set_geometry(va, va, self.ta)
        self.t.vertex_colors = self.model_list[0].atoms.colors
        m0 = Model('m0', self.session)
        m0.add([self.t])
        self.session.models.add([m0])

    def massing(self, seq=False, unit=1, refinement=3):
        self.tetrahedron_model(seq=[seq[0], seq[1], seq[2]])

        i = 0
        chain_index = [seq[1]]
        for model in self.model_list:
            if model.name not in self.model_ids:
                continue
            for chain in model.chains:
                if chain.chain_id not in self.chain_ids[model.name]:
                    continue
                if seq[1] < i < seq[2]:
                    chain_index.append(i)
                for amino_index in range(len(chain.residues)):
                    if chain.residues[amino_index] is None:
                        continue
                    i += 1
        chain_index.append(seq[2])

        print(chain_index, i)

        if not seq:
            seq = (0, 0, len(self.va) - 1)

        i = 0
        m = Model('m', self.session)
        k = Drawing("k")
        while i < len(chain_index) - 1:
            v = self.model_list[seq[0]].residues[chain_index[i]: chain_index[i + 1]].atoms.coords
            mesh = alphashape.alphashape(v, refinement * 0.1)
            inside = trimesh.proximity.ProximityQuery(mesh).signed_distance

            visited = set()
            count = 0

            # Create the first tetrahedron
            edge_length = self.avg_edge_length * unit
            id1 = chain_index[i]
            pt1 = self.va[id1][0]
            pt2 = self.va[id1][0] + (self.va[id1][1] - self.va[id1][0]) * edge_length / np.linalg.norm(self.va[id1][1] - self.va[id1][0])
            pt3 = self.va[id1][0] + (self.va[id1][2] - self.va[id1][0]) * edge_length / np.linalg.norm(self.va[id1][2] - self.va[id1][0])
            pt4 = self.va[id1][0] + (self.va[id1][3] - self.va[id1][0]) * edge_length / np.linalg.norm(self.va[id1][3] - self.va[id1][0])

            self.massing_vertices = [[pt1, pt2, pt3, pt4]]
            f = list(combinations(np.arange(count * 4, (count + 1) * 4), 3))
            faces = f

            pt1, pt2, pt3, pt4 = tuple(pt1), tuple(pt2), tuple(pt3), tuple(pt4)
            q = [{pt1, pt2, pt3, pt4}]
            t = tuple(sorted((pt1, pt2, pt3, pt4)))
            visited.add(t)

            depth = 10**7
            while q:
                if depth < 0:
                    break
                depth -= 1

                # Create new four tetrahedrons
                prev_tetra = list(q.pop())
                combine = combinations(prev_tetra, 3)
                for p in combine:
                    for x in prev_tetra:
                        if x not in p:
                            p += (x,)
                            break

                    pt1, pt2, pt3, pt4 = p
                    pt1, pt2, pt3, pt4 = np.array(pt1), np.array(pt2), np.array(pt3), np.array(pt4)
                    p1 = pt2
                    p2 = 2 * pt2 - pt1
                    p3 = pt2 + pt3 - pt1
                    p4 = pt2 + pt4 - pt1
                    centroid = (p1 + p2 + p3 + p4) / 4

                    # Out of boundary
                    if inside((centroid,)) < -5 * unit:
                        continue

                    # Visited or Not
                    pt1, pt2, pt3, pt4 = tuple(p1), tuple(p2), tuple(p3), tuple(p4)
                    t = tuple(sorted((pt1, pt2, pt3, pt4)))
                    if t not in visited:
                        pt1, pt2, pt3, pt4 = np.array(pt1, dtype=np.longdouble), np.array(pt2, dtype=np.longdouble),\
                                             np.array(pt3, dtype=np.longdouble), np.array(pt4, dtype=np.longdouble)

                        self.massing_vertices.append([pt1, pt2, pt3, pt4])
                        f = list(combinations(np.arange(count * 4, (count + 1) * 4), 3))
                        faces.extend(f)
                        count += 1

                        pt1, pt2, pt3, pt4 = tuple(pt1), tuple(pt2), tuple(pt3), tuple(pt4)
                        q.append({pt1, pt2, pt3, pt4})
                        visited.add(t)

            # Refine the massing Tetras within the Boundary
            x = 0
            while x < len(self.massing_vertices):
                pt1, pt2, pt3, pt4 = self.massing_vertices[x]

                centroid = (pt1 + pt2 + pt3 + pt4) / 4
                if inside((centroid,)) < 0:
                    self.massing_vertices.pop(x)
                else:
                    x += 1

            self.massing_vertices = np.array(self.massing_vertices)
            self.massing_vertices = np.reshape(self.massing_vertices, (self.massing_vertices.shape[0] * 4, self.massing_vertices.shape[2]))
            faces = np.array(faces, np.int32)

            t = Drawing("t")
            t.set_geometry(self.massing_vertices, self.massing_vertices, faces)
            t.vertex_colors = np.array([colors[i % len(colors)] for p in range(len(self.massing_vertices))], dtype=np.int8)
            k.add_drawing(t)
            i += 1

        m.add([k])
        self.session.models.add([m])

        m2 = Model('m2', self.session)
        # Attach massing model to the tetrahedron protein model
        if seq[2] + 1 < len(self.va):
            pt1 = self.va[seq[2] + 2][0]
            nearest_pt2 = self.massing_vertices[0]

            min_dist = np.linalg.norm(nearest_pt2 - pt1)
            for pt2 in self.massing_vertices:
                if np.linalg.norm(pt1 - pt2) < min_dist:
                    nearest_pt2 = pt2
                    min_dist = np.linalg.norm(pt1 - pt2)

            vec = pt1 - nearest_pt2
            perp_dir = np.array([-1 / vec[0], 1 / vec[1], 0])
            perp_dir /= np.linalg.norm(perp_dir)
            mag = (self.avg_edge_length ** 2 - ((np.linalg.norm(vec)) ** 2) * 0.25) ** 0.5
            perp_dir *= mag

            pt1 = self.va[seq[2] + 2][0]
            pt2 = (pt1 + nearest_pt2) / 2 + perp_dir

            vec = pt2 - pt1
            perp_dir = np.array([-1 / vec[0], 1 / vec[1], 0])
            perp_dir /= np.linalg.norm(perp_dir)
            pt3 = (pt1 + pt2) / 2 + ht2 * self.avg_edge_length * perp_dir

            unit_dir = np.cross(pt2 - pt1, pt3 - pt1)
            unit_dir /= np.linalg.norm(unit_dir)
            pt4 = (pt1 + pt2 + pt3) / 3 + ht3 * self.avg_edge_length * unit_dir

            pt5 = pt2
            pt6 = nearest_pt2

            vec = pt6 - pt5
            perp_dir = np.array([-1 / vec[0], 1 / vec[1], 0])
            perp_dir /= np.linalg.norm(perp_dir)
            pt7 = (pt5 + pt6) / 2 + ht2 * self.avg_edge_length * perp_dir

            unit_dir = np.cross(pt6 - pt5, pt7 - pt5)
            unit_dir /= np.linalg.norm(unit_dir)
            pt8 = (pt5 + pt6 + pt7) / 3 + ht3 * self.avg_edge_length * unit_dir

            add = np.array([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8])
            add_faces = np.array([[0, 1, 2], [1, 2, 3], [1, 0, 3], [2, 0, 3], [4, 5, 6], [5, 6, 7], [5, 4, 7], [4, 6, 7]])

        elif seq[2] + 1 == len(self.va):
            pt1 = self.va[seq[2]][0]
            nearest_pt2 = self.massing_vertices[0]

            min_dist = np.linalg.norm(nearest_pt2 - pt1)
            for pt2 in self.massing_vertices:
                if np.linalg.norm(pt1 - pt2) < min_dist:
                    nearest_pt2 = pt2
                    min_dist = np.linalg.norm(pt1 - pt2)

            d = (pt1 - nearest_pt2)
            d /= np.linalg.norm(d)
            pt1 = nearest_pt2
            pt2 = pt1 + d * self.avg_edge_length

            vec = pt2 - pt1
            perp_dir = np.array([-1 / vec[0], 1 / vec[1], 0])
            perp_dir /= np.linalg.norm(perp_dir)
            pt3 = (pt1 + pt2) / 2 + ht2 * self.avg_edge_length * perp_dir

            unit_dir = np.cross(pt2 - pt1, pt3 - pt1)
            unit_dir /= np.linalg.norm(unit_dir)
            pt4 = (pt1 + pt2 + pt3) / 3 + ht3 * self.avg_edge_length * unit_dir

            add = np.array([pt1, pt2, pt3, pt4])
            add_faces = np.array([[0, 1, 2], [1, 2, 3], [1, 0, 3], [2, 0, 3]])

        if seq[2] + 1 <= len(self.va):
            k = Drawing("k")
            k.set_geometry(add, add, faces)
            k.vertex_colors = np.array([[88, 110, 255, 255] for i in range(8)], dtype=np.int8)

            m2.add([k])
            self.session.models.add([m2])

        self.va = []
