import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'simplyenergy',
    label: 'Simply Energy Colours',
    colors: ['#2CC5F3', '#00A3E2', '#006CB7', '#FDF859', '#62A833'],
  },
].map(s => new CategoricalScheme(s));

export default schemes;
