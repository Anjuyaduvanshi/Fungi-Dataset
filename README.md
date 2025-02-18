#  Fungi Growth Image Generator

This project generates synthetic images of fungi growth stages (spores, hyphae, and mycelium) based on JSON input.

### Growth Stages

1. **Spore Stage**:
   - Small, randomly distributed spores representing the initial stage of fungi.
   - Color: Bright yellow, symbolizing the vitality of fresh spores.

2. **Hyphal Growth**:
   - Branching structures (hyphae) emerge from the spores, creating a web-like network.
   - The branches grow recursively with dynamic angles, lengths, and widths.
   - Color: Gradually transitions from yellow to orange tones.

3. **Mycelium Formation**:
   - Dense fungal networks form, completing the fungi's life cycle.
   - Growth is influenced by temperature and environmental factors.
   - Color: Deep red hues represent mature fungal structures.

### Features
- Generates synthetic fungi images using branching structures.
- Supports three classes: spore, hyphae, mycelium.
- Applies color interpolation to simulate realistic growth.
- Uses temperature-dependent transformations.
- Splits generated images into train, validation, and test sets.
---
### Requirements
Ensure you have the following dependencies installed:

pip install matplotlib numpy

### Usage
Prepare Input JSON

The JSON file should contain entries like:


[

    {"class_label": "spore", "description": "Early fungal spore"},
    
    {"class_label": "hyphae", "description": "Growing hyphae structure"},
    
    {"class_label": "mycelium", "description": "Mature fungal network"}
]

### Run the Script

python generator.py

### Output
- Generated images are saved in the specified output directory.
- Data is split into train, val, and test.
- JSON metadata is generated for each dataset split.
---
## Mathematical Representation

1. **Branch Length Scaling**: 
- Normal distribution with mean=1 and standard deviation=0.2.

2. **Dynamic Color Interpolation**: 
- Smooth transitions from yellow to orange to red based on growth factor.

3. **Growth Factor**: 
- Scales the transition from hyphae to mycelium.

4. **Recursive Depth**: 
- Branching depth reduces over iterations, limiting the recursion.
---
## Dataset Features

### Visual Transition
- Early stages: Bright yellow spores.
- Intermediate stages: Orange branching hyphae.
- Final stages: Dense, red mycelium.

### Environmental Factors
- Random perturbations influence branching and growth.

### Image Resolution
- High-resolution images (15x15 grid), suitable for visualization and analysis.
---
## Applications
This dataset is suitable for:

- Machine Learning: Training models to classify fungal growth stages.

- Biological Simulation: Studying growth patterns in fungi.

- Art and Design: Generating biologically inspired visuals.
---
## Research Paper

To support the study of these time-dependent processes, we present a synthetic, time-aligned image dataset that models key stages of fungal growth. This dataset captures spore size reduction, branching dynamics, and the emergence of complex mycelium networks.

---
## License

This project is open-source and can be modified for research or educational use.

## Contributing

Contributions are welcome! Feel free to:
- Open issues for suggestions or bugs.
- Submit pull requests for improvements or additional features.

## Acknowledgments

This dataset generation script is inspired by the complexity and beauty of fungal growth patterns, blending biology and computational modeling.

