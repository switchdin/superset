/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import airbnb from '@superset-ui/core/lib/color/colorSchemes/categorical/airbnb';
import categoricalD3 from '@superset-ui/core/lib/color/colorSchemes/categorical/d3';
import echarts from '@superset-ui/core/lib/color/colorSchemes/categorical/echarts';
import google from '@superset-ui/core/lib/color/colorSchemes/categorical/google';
import lyft from '@superset-ui/core/lib/color/colorSchemes/categorical/lyft';
import preset from '@superset-ui/core/lib/color/colorSchemes/categorical/preset';
import sequentialCommon from '@superset-ui/core/lib/color/colorSchemes/sequential/common';
import sequentialD3 from '@superset-ui/core/lib/color/colorSchemes/sequential/d3';
import {
  CategoricalScheme,
  getCategoricalSchemeRegistry,
  getSequentialSchemeRegistry,
  SequentialScheme,
} from '@superset-ui/core';
import superset from '@superset-ui/core/lib/color/colorSchemes/categorical/superset';
   
const schemes = [
  {
    id: 'switchdinColors',
    label: 'SwitchDin Colors',
    colors: [ '#00B299','#40C5B2','#80D8CC','#C0EBE5','#CDD0D2','#9BA0A4','#697177','#37424A'],
  },
  {
    id: 'yurikaColors',
    label: 'Yurika Colors',
    colors: [ "#5e2590",
              "#b12d76",
              "#f03f52",
              "#F37229",
              "#a13421",
             ],
  },
  {
    id: 'jacanaColors',
    label: 'Jacana Colors',
    colors: [ "#b8c496",
              "#D9C796",
              "#F3643D",
              "#F68224",
              "#213E52",
             ],
  },
  {
    id: 'simplyColors',
    label: 'Simply Colors',
    colors: [ "#2CC5F3",
              "#00A3E2",
              "#006CB7",
              "#FDF859",
              "#62A833",
             ],
  },
  {
    id: 'ausgridColors',
    label: 'Ausgrid Colors',
    colors: [ "#73B818",
              "#69AC40",
              "#008BC0",
              "#006095",
              "#1D9CA6",
             ],
  },
  {
    id: 'originColors',
    label: 'Origin Colors',
    colors: [ "#FF373C",
              "#FA4616",
              "#FF8133",
              "#FFB92D",
              "#D44500",
             ],
  },
  {
    id: 'sapnColors',
    label: 'SAPN Colors',
    colors: [ "#284051",
              "#1F4C71",
              "#FA7A0A",
              "#535353",
              "#1A1614",
             ],
  },
].map(s => new CategoricalScheme(s));

export default function setupColors(
  extraCategoricalColorSchemas: CategoricalScheme[] = [],
  extraSequentialColorSchemes: SequentialScheme[] = [],
) {
  // Register color schemes
  const categoricalSchemeRegistry = getCategoricalSchemeRegistry();

  if (extraCategoricalColorSchemas?.length > 0) {
    extraCategoricalColorSchemas.forEach(scheme => {
      categoricalSchemeRegistry.registerValue(scheme.id, scheme);
    });
  }

  [schemes, superset, airbnb, categoricalD3, echarts, google, lyft, preset].forEach(
    group => {
      group.forEach(scheme => {
        categoricalSchemeRegistry.registerValue(scheme.id, scheme);
      });
    },
  );
  categoricalSchemeRegistry.setDefaultKey('supersetColors');

  const sequentialSchemeRegistry = getSequentialSchemeRegistry();

  if (extraSequentialColorSchemes?.length > 0) {
    extraSequentialColorSchemes.forEach(scheme => {
      categoricalSchemeRegistry.registerValue(scheme.id, scheme);
    });
  }

  [sequentialCommon, sequentialD3].forEach(group => {
    group.forEach(scheme => {
      sequentialSchemeRegistry.registerValue(scheme.id, scheme);
    });
  });
  sequentialSchemeRegistry.setDefaultKey('superset_seq_1');
}
