# Copyright (c) 2019-2022, RTE (https://www.rte-france.com)
# See AUTHORS.txt and https://github.com/rte-france/Grid2Op/pull/319
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of Grid2Op, Grid2Op a testbed platform to model sequential decision making in power systems.

import pdb
import grid2op
import unittest
import warnings

from grid2op.tests.helper_path_test import *


class Issue367Tester(unittest.TestCase):
    def setUp(self) -> None:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            self.env = grid2op.make("l2rpn_wcci_2022", test=True)
        self.env.set_id(2)
        self.obs = self.env.reset()

    def tearDown(self) -> None:
        self.env.close()
        return super().tearDown()
    
    def test_action(self):
        # set up any topology action, e.g., 
        # connect all elements in substation 1 to bus 2
        gen_id = 2
        sub_id = 1
        action = self.env.action_space()
        nb_el = type(self.env.action_space).sub_info[sub_id]
        arr_ = np.full(nb_el, fill_value=True, dtype=bool)
        action.sub_change_bus = [(sub_id, arr_)]
        obs_, _, done, _ = self.obs.simulate(action)

        print(self.obs.gen_p[gen_id])
        print(obs_.gen_p[gen_id])
        assert abs(obs_.gen_p[gen_id] - self.obs.gen_p[gen_id]) <= obs_.gen_max_ramp_up[gen_id]
        
    def tearDown(self) -> None:
        self.env.close()
        return super().tearDown()
    

if __name__ == "__main__":
    unittest.main()
