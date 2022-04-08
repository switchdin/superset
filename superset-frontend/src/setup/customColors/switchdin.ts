import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'switchdin',
    label: 'SwitchDin Colors',
    colors: [
      '#00B299',
      '#40C5B2',
      '#80D8CC',
      '#C0EBE5',
      '#CDD0D2',
      '#9BA0A4',
      '#697177',
      '#37424A',
    ],
  },
].map(s => new CategoricalScheme(s));

export default schemes;
