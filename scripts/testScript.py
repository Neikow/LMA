# trace generated using paraview version 5.5.0

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3ReaderS'
resultsxmf = Xdmf3ReaderS(FileName=['C:\\Users\\Vitaly\\OneDrive\\Bureau\\LMA\\results\\barrage1\\res\\results.xmf'])
resultsxmf.PointArrays = ['Accel', 'Alpha', 'Dens', 'Displ', 'Dom', 'Jac', 'Kappa', 'Lamb', 'Mass', 'Mu', 'Veloc']
resultsxmf.CellArrays = ['Mat', 'Proc']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on resultsxmf
resultsxmf.PointArrays = ['Accel', 'Displ', 'Mass', 'Veloc']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [1735, 802]

# show data in view
resultsxmfDisplay = Show(resultsxmf, renderView1)

# get color transfer function/color map for 'Mass'
massLUT = GetColorTransferFunction('Mass')

# get opacity transfer function/opacity map for 'Mass'
massPWF = GetOpacityTransferFunction('Mass')

# trace defaults for the display properties.
resultsxmfDisplay.Representation = 'Surface'
resultsxmfDisplay.ColorArrayName = ['POINTS', 'Mass']
resultsxmfDisplay.LookupTable = massLUT
resultsxmfDisplay.OSPRayScaleArray = 'Mass'
resultsxmfDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
resultsxmfDisplay.SelectOrientationVectors = 'Displ'
resultsxmfDisplay.ScaleFactor = 228.0
resultsxmfDisplay.SelectScaleArray = 'Mass'
resultsxmfDisplay.GlyphType = 'Arrow'
resultsxmfDisplay.GlyphTableIndexArray = 'Mass'
resultsxmfDisplay.GaussianRadius = 11.4
resultsxmfDisplay.SetScaleArray = ['POINTS', 'Mass']
resultsxmfDisplay.ScaleTransferFunction = 'PiecewiseFunction'
resultsxmfDisplay.OpacityArray = ['POINTS', 'Mass']
resultsxmfDisplay.OpacityTransferFunction = 'PiecewiseFunction'
resultsxmfDisplay.DataAxesGrid = 'GridAxesRepresentation'
resultsxmfDisplay.SelectionCellLabelFontFile = ''
resultsxmfDisplay.SelectionPointLabelFontFile = ''
resultsxmfDisplay.PolarAxes = 'PolarAxesRepresentation'
resultsxmfDisplay.ScalarOpacityFunction = massPWF
resultsxmfDisplay.ScalarOpacityUnitDistance = 13.750920297594181

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
resultsxmfDisplay.ScaleTransferFunction.Points = [1.7380671124556102e-08, 0.0, 0.5, 0.0, 2.24006724357605, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
resultsxmfDisplay.OpacityTransferFunction.Points = [1.7380671124556102e-08, 0.0, 0.5, 0.0, 2.24006724357605, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
resultsxmfDisplay.DataAxesGrid.XTitleFontFile = ''
resultsxmfDisplay.DataAxesGrid.YTitleFontFile = ''
resultsxmfDisplay.DataAxesGrid.ZTitleFontFile = ''
resultsxmfDisplay.DataAxesGrid.XLabelFontFile = ''
resultsxmfDisplay.DataAxesGrid.YLabelFontFile = ''
resultsxmfDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
resultsxmfDisplay.PolarAxes.PolarAxisTitleFontFile = ''
resultsxmfDisplay.PolarAxes.PolarAxisLabelFontFile = ''
resultsxmfDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
resultsxmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
resultsxmfDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(resultsxmfDisplay, ('POINTS', 'Veloc', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(massLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
resultsxmfDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
resultsxmfDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Veloc'
velocLUT = GetColorTransferFunction('Veloc')

# Rescale transfer function
velocLUT.RescaleTransferFunction(0.0, 1e-09)

# get opacity transfer function/opacity map for 'Veloc'
velocPWF = GetOpacityTransferFunction('Veloc')

# Rescale transfer function
velocPWF.RescaleTransferFunction(0.0, 1e-09)

# reset view to fit data
renderView1.ResetCamera()

# animationScene1.Play()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [140.0, 5924.30901218659, 1002.5]
renderView1.CameraFocalPoint = [140.0, 55.0, 1002.5]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 1519.0889539457523

#### uncomment the following to render all views
RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

renderView1.Update()

for x in range(0, 20):
    filename = ''
    SaveScreenshot(filename, magnification=1, quality=100, view=renderView1)
    animationScene1.GoToNext()

animationScene1.GoToFirsst()

SaveAnimation('animation.avi', GetActiveView(),
              FrameWindow = [1, 20],
              FrameRate = 1)
