---
name: webgpu-threejs-tsl
description: TSL and WebGPU node-shader toolkit covering node materials, GPU compute, post-processing, and WGSL integration. Use when building Three.js WebGPU apps, writing TSL shaders or node materials, porting GLSL to TSL, authoring GPU compute shaders, or assembling post-processing effects.
tags: [create, design, engineering, transform]
---

# WebGPU Three.js with TSL

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

TSL (Three.js Shading Language) is a node-based shader abstraction that lets you write GPU shaders in JavaScript instead of GLSL/WGSL strings.

## Quick Start

```javascript
import * as THREE from 'three/webgpu';
import { color, time, oscSine } from 'three/tsl';

const renderer = new THREE.WebGPURenderer();
await renderer.init();

const material = new THREE.MeshStandardNodeMaterial();
material.colorNode = color(0xff0000).mul(oscSine(time));
```

## Skill Contents

Read the file matching the task; do not load all of them at once.

### Documentation

- `docs/core-concepts.md` - Types, operators, uniforms, control flow
- `docs/materials.md` - Node materials and all properties
- `docs/compute-shaders.md` - GPU compute with instanced arrays
- `docs/post-processing.md` - Built-in and custom effects
- `docs/wgsl-integration.md` - Custom WGSL functions
- `docs/device-loss.md` - Handling GPU device loss and recovery
- `docs/limits-and-features.md` - WebGPU device limits and optional features

### Examples

- `examples/basic-setup.js` - Minimal WebGPU project
- `examples/custom-material.js` - Custom shader material
- `examples/particle-system.js` - GPU compute particles
- `examples/post-processing.js` - Effect pipeline
- `examples/earth-shader.js` - Complete Earth with atmosphere

### Templates

- `templates/webgpu-project.js` - Starter project template
- `templates/compute-shader.js` - Compute shader template

### Reference

- `REFERENCE.md` - Quick reference cheatsheet

## Key Concepts

### Import Pattern

```javascript
// Always use the WebGPU entry point
import * as THREE from 'three/webgpu';
import { /* TSL functions */ } from 'three/tsl';
```

### Node Materials

Replace standard material properties with TSL nodes:

```javascript
material.colorNode = texture(map);        // instead of material.map
material.roughnessNode = float(0.5);      // instead of material.roughness
material.positionNode = displaced;         // vertex displacement
```

## Resources

- [Three.js TSL Wiki](https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language)
- [WebGPU Examples](https://github.com/mrdoob/three.js/tree/master/examples) (files prefixed with `webgpu_`)

Forked from [dgreenheck/webgpu-claude-skill](https://github.com/dgreenheck/webgpu-claude-skill).
