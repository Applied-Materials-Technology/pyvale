# Divertor Monoblock Heatsink Component
#

#-------------------------------------------------------------------------
#_* MOOSEHERDER VARIABLES - START

endTime = 20
timeStep = 5

coolantTemp=100.0      # degC
heatTransCoeff=125.0e3 # W.m^-2.K^-1
surfHeatFlux=10.0e6    # W.m^-2

# Copper-Chromium-Zirconium ITER SDC-IC pg.148 at 200degC
cucrzrDensity = 8816.0  # kg.m^-3
cucrzrThermCond = 343.0 # W.m^-1.K^-1
cucrzrSpecHeat = 407.0  # J.kg^-1.K^-1

# Pure Copper ITER SDC-IC pg.134 at 250degC
cuDensity = 8829.0  # kg.m^-3
cuThermCond = 384.0 # W.m^-1.K^-1
cuSpecHeat = 406.0  # J.kg^-1.K^-1

# Tungsten ITER SDC-IC pg.224 at 600degC
wDensity = 19150.0  # kg.m^-3
wThermCond = 127.0 # W.m^-1.K^-1
wSpecHeat = 147.0  # J.kg^-1.K^-1

#** MOOSEHERDER VARIABLES - END
#-------------------------------------------------------------------------

[Mesh]
  type = FileMesh
  file = 'monoblock_3d.msh'
[]

[Variables]
  [temperature]
    family = LAGRANGE
    order = SECOND
    initial_condition = ${coolantTemp}
  []
[]

[Kernels]
  [heat_conduction]
    type = HeatConduction
    variable = temperature
  []
  [time_derivative]
    type = HeatConductionTimeDerivative
    variable = temperature
  []
[]

[Materials]
  [cucrzr_thermal]
    type = HeatConductionMaterial
    thermal_conductivity = ${cucrzrThermCond}
    specific_heat = ${cucrzrSpecHeat}
    block = 'pipe-cucrzr'
  []

  [copper_thermal]
    type = HeatConductionMaterial
    thermal_conductivity = ${cuThermCond}
    specific_heat = ${cuSpecHeat}
    block = 'interlayer-cu'
  []

  [tungsten_thermal]
    type = HeatConductionMaterial
    thermal_conductivity = ${wThermCond}
    specific_heat = ${wSpecHeat}
    block = 'armour-w'
  []

  [cucrzr_density]
    type = GenericConstantMaterial
    prop_names = 'density'
    prop_values = ${cucrzrDensity}
    block = 'pipe-cucrzr'
  []

  [copper_density]
    type = GenericConstantMaterial
    prop_names = 'density'
    prop_values = ${cuDensity}
    block = 'interlayer-cu'
  []

  [tungsten_density]
    type = GenericConstantMaterial
    prop_names = 'density'
    prop_values = ${wDensity}
    block = 'armour-w'
  []
[]

[BCs]
  [heat_flux_in]
    type = FunctionNeumannBC
    variable = temperature
    boundary = 'bc-top-heatflux'
    function = '${fparse surfHeatFlux}*(1-exp(-t))'
  []

  [heat_flux_out]
    type = ConvectiveHeatFluxBC
    variable = temperature
    boundary = 'bc-pipe-heattransf'
    T_infinity = ${coolantTemp}
    heat_transfer_coefficient = ${heatTransCoeff}
  []
[]

[Preconditioning]
  [smp]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Transient
  solve_type = 'PJFNK'
  petsc_options_iname = '-pc_type -pc_hypre_type'
  petsc_options_value = 'hypre    boomeramg'
  end_time = ${endTime}
  dt = ${timeStep}
[]

[Postprocessors]
  [max_temp]
    type = ElementExtremeValue
    variable = temperature
  []
[]

[Outputs]
  exodus = true
[]
