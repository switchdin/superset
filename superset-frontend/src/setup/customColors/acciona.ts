import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'acciona',
    label: 'Acciona Colors',
    colors: ['#FF6464', '#FF0000', '#9B0000', '#7F7E7E', '#464646', '#000000'],
  },
].map(s => new CategoricalScheme(s));

export default schemes;