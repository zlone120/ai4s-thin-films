# AI for Thin Films - MLP Inverse Design

## Parameters
- target: target reflection peak wavelength (450~750 nm), formula: 450 + 10 * (N mod 31)
- seed: 6
- design_seed: 7

## Repository
https://github.com/zlone120/ai4s-thin-films

## Usage
```bash
pip install -r requirements.txt
python generate_data.py
python train_mlp.py
python inverse_design.py
python plot_results.py
```

## Project Structure
- `tmm_core.py` - Transfer Matrix Method implementation
- `generate_data.py` - Generate training dataset
- `train_mlp.py` - Train MLP model
- `inverse_design.py` - Inverse design prediction
- `plot_results.py` - Visualization
