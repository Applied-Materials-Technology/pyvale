#-------------------------------------------------------------------------
# pyvale: simple,2Dplate,2mat,thermomechanical,steady
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
#_* MOOSEHERDER VARIABLES - START

#endTime = 1
#timeStep = 1

# Geometric Properties
lengX = 100e-3  # m
lengY = 50e-3   # m

# Mesh Properties
nElemX = 20
nElemY = 10
eType = QUAD4 # QUAD4 for 1st order, QUAD8 for 2nd order

# Thermal Loads/BCs
uniformTemp = 200 # degC
#coolantTemp = 20.0      # degC
#heatTransCoeff = 125.0e3 # W.m^-2.K^-1
#surfHeatFlux = 500.0e3    # W.m^-2

# Material Properties:
# Thermal Props: Pure (OFHC) Copper at 250degC
cuDensity = 8829.0  # kg.m^-3
cuThermCond = 384.0 # W.m^-1.K^-1
cuSpecHeat = 406.0  # J.kg^-1.K^-1

# Thermal Props: Tungsten at 600degC
wDensity = 19150.0  # kg.m^-3
wThermCond = 127.0 # W.m^-1.K^-1
wSpecHeat = 147.0  # J.kg^-1.K^-1

# Mechanical Props: OFHC Copper at 250degC
cuEMod = 108e9       # Pa
cuPRatio = 0.33      # -

# Mechanical Props: Tungsten at 250degC
wEMod = 387e9       # Pa
wPRatio = 0.29      # -

# Thermo-mechanical coupling
stressFreeTemp = 20 # degC
cuThermExp = 17.8e-6 # 1/degC
wThermExp = 4.72e-6 # 1/degC

#** MOOSEHERDER VARIABLES - END
#-------------------------------------------------------------------------

# Selection tolerance for bounding box node selection
sTol = ${fparse lengX/(nElemX*4)}

[GlobalParams]
  displacements = 'disp_x disp_y'
[]

[Mesh]
  [generated_mesh]
    type = GeneratedMeshGenerator
    dim = 2
    nx = ${nElemX}
    ny = ${nElemY}
    xmax = ${lengX}
    ymax = ${lengY}
    elem_type = ${eType}
  []

  [block1]
    type = SubdomainBoundingBoxGenerator
    input = generated_mesh
    block_id = 1
    bottom_left = '0 0 0'
    top_right = '${fparse lengX/2} ${fparse lengY} 0'
  []
  [block2]
    type = SubdomainBoundingBoxGenerator
    input = block1
    block_id = 2
    bottom_left = '${fparse lengX/2} 0 0'
    top_right = '${fparse lengX} ${fparse lengY} 0'
  []

  [node_bottom_left]
    type = BoundingBoxNodeSetGenerator
    input = block2
    bottom_left = '${fparse 0-sTol}
                   ${fparse 0-sTol}
                   ${fparse 0-sTol}'
    top_right = '${fparse 0+sTol}
                 ${fparse 0+sTol}
                 ${fparse 0+sTol}'
    new_boundary = bottom_left_node
  []
  [node_top_left]
      type = BoundingBoxNodeSetGenerator
      input = node_bottom_left
      bottom_left = '${fparse 0-sTol}
                    ${fparse lengY-sTol}
                    ${fparse 0-sTol}'
      top_right = '${fparse 0+sTol}
                  ${fparse lengY+sTol}
                  ${fparse 0+sTol}'
      new_boundary = top_left_node
  []
  [node_bottom_right]
      type = BoundingBoxNodeSetGenerator
      input = node_top_left
      bottom_left = '${fparse lengX-sTol}
                    ${fparse 0-sTol}
                    ${fparse 0-sTol}'
      top_right = '${fparse lengX+sTol}
                  ${fparse 0+sTol}
                  ${fparse 0+sTol}'
      new_boundary = bottom_right_node
  []

  [full_plate_nodeset]
    type = BoundingBoxNodeSetGenerator
    input = node_bottom_right
    bottom_left = '${fparse 0-sTol}
                  ${fparse 0-sTol}
                  ${fparse 0-sTol}'
    top_right = '${fparse lengX+sTol}
                ${fparse lengY+sTol}
                ${fparse 0+sTol}'
    new_boundary = full_plate
  []
[]

[Variables]
  [temperature]
    family = LAGRANGE
    order = FIRST
    initial_condition = ${uniformTemp}
  []
[]

[Kernels]
  [heat_conduction]
    type = HeatConduction
    variable = temperature
  []
  #[time_derivative]
  #    type = HeatConductionTimeDerivative
  #    variable = temperature
  #[]
[]

[Modules/TensorMechanics/Master]
  [all]
      add_variables = true
      #material_output_family = MONOMIAL   # MONOMIAL, LAGRANGE
      #material_output_order = FIRST       # CONSTANT, FIRST, SECOND,
      strain = SMALL                     # SMALL or FINITE
      automatic_eigenstrain_names = true
      generate_output = 'vonmises_stress stress_xx stress_yy stress_xy strain_xx strain_yy strain_xy'
  []
[]

[Materials]
  [copper_thermal]
    type = HeatConductionMaterial
    thermal_conductivity = ${cuThermCond}
    specific_heat = ${cuSpecHeat}
    block = 1
  []
  [copper_density]
    type = GenericConstantMaterial
    prop_names = 'density'
    prop_values = ${cuDensity}
    block = 1
  []
  [copper_elasticity]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${cuEMod}
    poissons_ratio = ${cuPRatio}
    block = 1
  []
  [copper_expansion]
    type = ComputeThermalExpansionEigenstrain
    temperature = temperature
    stress_free_temperature = ${stressFreeTemp}
    thermal_expansion_coeff = ${cuThermExp}
    eigenstrain_name = thermal_expansion_eigenstrain
    block = 1
  []

  [tungsten_thermal]
    type = HeatConductionMaterial
    thermal_conductivity = ${wThermCond}
    specific_heat = ${wSpecHeat}
    block = 2
  []
  [tungsten_density]
    type = GenericConstantMaterial
    prop_names = 'density'
    prop_values = ${wDensity}
    block = 2
  []
  [tungsten_elasticity]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${wEMod}
    poissons_ratio = ${wPRatio}
    block = 2
  []
  [tungsten_expansion]
    type = ComputeThermalExpansionEigenstrain
    temperature = temperature
    stress_free_temperature = ${stressFreeTemp}
    thermal_expansion_coeff = ${wThermExp}
    eigenstrain_name = thermal_expansion_eigenstrain
    block = 2
  []

  [stress]
    type = ComputeLinearElasticStress # ComputeLinearElasticStress or ComputeFiniteStrainElasticStress
  []
[]

[BCs]
  [uniform_temp]
    type = DirichletBC
    variable = temperature
    boundary = 'full_plate'
    value = ${uniformTemp}
  []

  [bottom_left_disp_x]
    type = DirichletBC
    variable = disp_x
    boundary = 'bottom_left_node'
    value = 0
  []
  [bottom_left_disp_y]
      type = DirichletBC
      variable = disp_y
      boundary = 'bottom_left_node'
      value = 0
  []
  [bottom_right_disp_y]
      type = DirichletBC
      variable = disp_y
      boundary = 'bottom_right_node'
      value = 0
  []
  [top_left_disp_x]
      type = DirichletBC
      variable = disp_x
      boundary = 'top_left_node'
      value = 0
  []

  #[left_disp_y]
  #    type = DirichletBC
  #    variable = disp_y
  #    boundary = 'left'
  #    value = 0
  #[]
  #[left_disp_x]
  #    type = DirichletBC
  #    variable = disp_x
  #    boundary = 'left'
  #    value = 0
  #[]
[]

[Preconditioning]
  [smp]
      type = SMP
      full = true
  []
[]

[Executioner]
  type = Steady
  solve_type = 'PJFNK'
  petsc_options_iname = '-pc_type -pc_hypre_type'
  petsc_options_value = 'hypre    boomeramg'
  #end_time= ${endTime}
  #dt = ${timeStep}
[]

[Postprocessors]
  [max_temp]
      type = NodalExtremeValue
      variable = temperature
  []
  [avg_temp]
      type = AverageNodalVariableValue
      variable = temperature
  []

  [max_x_disp]
      type = NodalExtremeValue
      variable = disp_x
  []
  [max_xx_strain]
      type = ElementExtremeValue
      variable = strain_xx
  []
  [avg_xx_strain]
      type = ElementAverageValue
      variable = strain_yy
  []
[]

[Outputs]
  exodus = true
[]