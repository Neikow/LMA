from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

ORIGIN = [13950, 12336, 12805]
DAM_POS = [13950, 12493.8, 12740.5]

# create a new 'Xdmf3ReaderS'
resultsxmf = Xdmf3ReaderS(FileName=['C:\\Users\\Vitaly\\OneDrive\\Bureau\\LMA\\results\\fast\\sem\\res\\results.xmf'])
# resultsxmf = Xdmf3ReaderS(FileName=['/scratch/vlysen/sims/20_08_dam_topo_but_shit/res/results.xmf'])
resultsxmf.PointArrays = ['Accel', 'Alpha', 'Dens', 'Displ', 'Dom', 'Jac', 'Kappa', 'Lamb', 'Mass', 'Mu', 'Press_gll', 'Veloc']
resultsxmf.CellArrays = ['Mat', 'Press_elem', 'Proc']

# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on resultsxmf
resultsxmf.PointArrays = ['Veloc']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1642, 1105]

# show data in view
resultsxmfDisplay = Show(resultsxmf, renderView1)

# get color transfer function/color map for 'Press_elem'
press_elemLUT = GetColorTransferFunction('Press_elem')

# get opacity transfer function/opacity map for 'Press_elem'
press_elemPWF = GetOpacityTransferFunction('Press_elem')

# trace defaults for the display properties.
resultsxmfDisplay.Representation = 'Surface'
resultsxmfDisplay.ColorArrayName = ['CELLS', 'Press_elem']
resultsxmfDisplay.LookupTable = press_elemLUT
resultsxmfDisplay.OSPRayScaleArray = 'Displ'
resultsxmfDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
resultsxmfDisplay.SelectOrientationVectors = 'Displ'
resultsxmfDisplay.ScaleFactor = 2790.0
resultsxmfDisplay.SelectScaleArray = 'Press_elem'
resultsxmfDisplay.GlyphType = 'Arrow'
resultsxmfDisplay.GlyphTableIndexArray = 'Press_elem'
resultsxmfDisplay.GaussianRadius = 139.5
resultsxmfDisplay.SetScaleArray = ['POINTS', 'Displ']
resultsxmfDisplay.ScaleTransferFunction = 'PiecewiseFunction'
resultsxmfDisplay.OpacityArray = ['POINTS', 'Displ']
resultsxmfDisplay.OpacityTransferFunction = 'PiecewiseFunction'
resultsxmfDisplay.DataAxesGrid = 'GridAxesRepresentation'
resultsxmfDisplay.SelectionCellLabelFontFile = ''
resultsxmfDisplay.SelectionPointLabelFontFile = ''
resultsxmfDisplay.PolarAxes = 'PolarAxesRepresentation'
resultsxmfDisplay.ScalarOpacityFunction = press_elemPWF
resultsxmfDisplay.ScalarOpacityUnitDistance = 112.50859023439013

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
resultsxmfDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
resultsxmfDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

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
# renderView1.Update()

# create a new 'Clip'
clip1 = Clip(Input=resultsxmf)
clip1.ClipType = 'Plane'
clip1.Scalars = ['CELLS', 'Press_elem']

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = ORIGIN

# Properties modified on clip1.ClipType
clip1.ClipType.Offset = 10000.0

# show data in view
clip1Display = Show(clip1, renderView1)

# trace defaults for the display properties.
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = ['CELLS', 'Press_elem']
clip1Display.LookupTable = press_elemLUT
clip1Display.OSPRayScaleArray = 'Displ'
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.SelectOrientationVectors = 'Displ'
clip1Display.ScaleFactor = 2561.0
clip1Display.SelectScaleArray = 'Press_elem'
clip1Display.GlyphType = 'Arrow'
clip1Display.GlyphTableIndexArray = 'Press_elem'
clip1Display.GaussianRadius = 128.05
clip1Display.SetScaleArray = ['POINTS', 'Displ']
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityArray = ['POINTS', 'Displ']
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.SelectionCellLabelFontFile = ''
clip1Display.SelectionPointLabelFontFile = ''
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityFunction = press_elemPWF
clip1Display.ScalarOpacityUnitDistance = 104.96111891230962

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip1Display.DataAxesGrid.XTitleFontFile = ''
clip1Display.DataAxesGrid.YTitleFontFile = ''
clip1Display.DataAxesGrid.ZTitleFontFile = ''
clip1Display.DataAxesGrid.XLabelFontFile = ''
clip1Display.DataAxesGrid.YLabelFontFile = ''
clip1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip1Display.PolarAxes.PolarAxisTitleFontFile = ''
clip1Display.PolarAxes.PolarAxisLabelFontFile = ''
clip1Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(resultsxmf, renderView1)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
# renderView1.Update()

# create a new 'Clip'
clip2 = Clip(Input=clip1)
clip2.ClipType = 'Plane'
clip2.Scalars = ['CELLS', 'Press_elem']

# Properties modified on clip2.ClipType
clip2.ClipType.Origin = ORIGIN
clip2.ClipType.Normal = [-1.0, 0.0, 0.0]
clip2.ClipType.Offset = 10000.0

# show data in view
clip2Display = Show(clip2, renderView1)

# trace defaults for the display properties.
clip2Display.Representation = 'Surface'
clip2Display.ColorArrayName = ['CELLS', 'Press_elem']
clip2Display.LookupTable = press_elemLUT
clip2Display.OSPRayScaleArray = 'Displ'
clip2Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip2Display.SelectOrientationVectors = 'Displ'
clip2Display.ScaleFactor = 2561.0
clip2Display.SelectScaleArray = 'Press_elem'
clip2Display.GlyphType = 'Arrow'
clip2Display.GlyphTableIndexArray = 'Press_elem'
clip2Display.GaussianRadius = 128.05
clip2Display.SetScaleArray = ['POINTS', 'Displ']
clip2Display.ScaleTransferFunction = 'PiecewiseFunction'
clip2Display.OpacityArray = ['POINTS', 'Displ']
clip2Display.OpacityTransferFunction = 'PiecewiseFunction'
clip2Display.DataAxesGrid = 'GridAxesRepresentation'
clip2Display.SelectionCellLabelFontFile = ''
clip2Display.SelectionPointLabelFontFile = ''
clip2Display.PolarAxes = 'PolarAxesRepresentation'
clip2Display.ScalarOpacityFunction = press_elemPWF
clip2Display.ScalarOpacityUnitDistance = 98.0382364407253

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip2Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip2Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip2Display.DataAxesGrid.XTitleFontFile = ''
clip2Display.DataAxesGrid.YTitleFontFile = ''
clip2Display.DataAxesGrid.ZTitleFontFile = ''
clip2Display.DataAxesGrid.XLabelFontFile = ''
clip2Display.DataAxesGrid.YLabelFontFile = ''
clip2Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip2Display.PolarAxes.PolarAxisTitleFontFile = ''
clip2Display.PolarAxes.PolarAxisLabelFontFile = ''
clip2Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
clip2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
# renderView1.Update()

# create a new 'Clip'
clip3 = Clip(Input=clip2)
clip3.ClipType = 'Plane'
clip3.Scalars = ['CELLS', 'Press_elem']

# init the 'Plane' selected for 'ClipType'
clip3.ClipType.Origin = ORIGIN

# Properties modified on clip3.ClipType
clip3.ClipType.Normal = [0.0, 0.0, 1.0]
clip3.ClipType.Offset = 10000.0

# Properties modified on clip3.ClipType
clip3.ClipType.Normal = [0.0, 0.0, 1.0]
clip3.ClipType.Offset = 10000.0

# show data in view
clip3Display = Show(clip3, renderView1)

# trace defaults for the display properties.
clip3Display.Representation = 'Surface'
clip3Display.ColorArrayName = ['CELLS', 'Press_elem']
clip3Display.LookupTable = press_elemLUT
clip3Display.OSPRayScaleArray = 'Displ'
clip3Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip3Display.SelectOrientationVectors = 'Displ'
clip3Display.ScaleFactor = 2280.5
clip3Display.SelectScaleArray = 'Press_elem'
clip3Display.GlyphType = 'Arrow'
clip3Display.GlyphTableIndexArray = 'Press_elem'
clip3Display.GaussianRadius = 114.025
clip3Display.SetScaleArray = ['POINTS', 'Displ']
clip3Display.ScaleTransferFunction = 'PiecewiseFunction'
clip3Display.OpacityArray = ['POINTS', 'Displ']
clip3Display.OpacityTransferFunction = 'PiecewiseFunction'
clip3Display.DataAxesGrid = 'GridAxesRepresentation'
clip3Display.SelectionCellLabelFontFile = ''
clip3Display.SelectionPointLabelFontFile = ''
clip3Display.PolarAxes = 'PolarAxesRepresentation'
clip3Display.ScalarOpacityFunction = press_elemPWF
clip3Display.ScalarOpacityUnitDistance = 91.80827629337975

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip3Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip3Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip3Display.DataAxesGrid.XTitleFontFile = ''
clip3Display.DataAxesGrid.YTitleFontFile = ''
clip3Display.DataAxesGrid.ZTitleFontFile = ''
clip3Display.DataAxesGrid.XLabelFontFile = ''
clip3Display.DataAxesGrid.YLabelFontFile = ''
clip3Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip3Display.PolarAxes.PolarAxisTitleFontFile = ''
clip3Display.PolarAxes.PolarAxisLabelFontFile = ''
clip3Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip3Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(clip2, renderView1)

# show color bar/color legend
clip3Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
# renderView1.Update()

# create a new 'Clip'
clip4 = Clip(Input=clip3)
clip4.ClipType = 'Plane'
clip4.Scalars = ['CELLS', 'Press_elem']

# init the 'Plane' selected for 'ClipType'
clip4.ClipType.Origin = [13950.0, 12546.642578125, 11402.5]

# set active source
SetActiveSource(clip3)

# set active source
SetActiveSource(clip4)

# Properties modified on clip4.ClipType
clip4.ClipType.Origin = ORIGIN
clip4.ClipType.Normal = [0.0, 0.0, -1.0]
clip4.ClipType.Offset = 10000.0

# show data in view
clip4Display = Show(clip4, renderView1)

# trace defaults for the display properties.
clip4Display.Representation = 'Surface'
clip4Display.ColorArrayName = ['CELLS', 'Press_elem']
clip4Display.LookupTable = press_elemLUT
clip4Display.OSPRayScaleArray = 'Displ'
clip4Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip4Display.SelectOrientationVectors = 'Displ'
clip4Display.ScaleFactor = 2000.0
clip4Display.SelectScaleArray = 'Press_elem'
clip4Display.GlyphType = 'Arrow'
clip4Display.GlyphTableIndexArray = 'Press_elem'
clip4Display.GaussianRadius = 100.0
clip4Display.SetScaleArray = ['POINTS', 'Displ']
clip4Display.ScaleTransferFunction = 'PiecewiseFunction'
clip4Display.OpacityArray = ['POINTS', 'Displ']
clip4Display.OpacityTransferFunction = 'PiecewiseFunction'
clip4Display.DataAxesGrid = 'GridAxesRepresentation'
clip4Display.SelectionCellLabelFontFile = ''
clip4Display.SelectionPointLabelFontFile = ''
clip4Display.PolarAxes = 'PolarAxesRepresentation'
clip4Display.ScalarOpacityFunction = press_elemPWF
clip4Display.ScalarOpacityUnitDistance = 85.90104845714319

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip4Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip4Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip4Display.DataAxesGrid.XTitleFontFile = ''
clip4Display.DataAxesGrid.YTitleFontFile = ''
clip4Display.DataAxesGrid.ZTitleFontFile = ''
clip4Display.DataAxesGrid.XLabelFontFile = ''
clip4Display.DataAxesGrid.YLabelFontFile = ''
clip4Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip4Display.PolarAxes.PolarAxisTitleFontFile = ''
clip4Display.PolarAxes.PolarAxisLabelFontFile = ''
clip4Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip4Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(clip3, renderView1)

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
# renderView1.Update()

# create a new 'Clip'
clip5 = Clip(Input=clip4)
clip5.ClipType = 'Plane'
clip5.Scalars = ['CELLS', 'Press_elem']

# Properties modified on clip5.ClipType
clip5.ClipType.Origin = ORIGIN
clip5.ClipType.Normal = [0.0, -1.0, 0.0]

# show data in view
clip5Display = Show(clip5, renderView1)

# trace defaults for the display properties.
clip5Display.Representation = 'Surface'
clip5Display.ColorArrayName = ['CELLS', 'Press_elem']
clip5Display.LookupTable = press_elemLUT
clip5Display.OSPRayScaleArray = 'Displ'
clip5Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip5Display.SelectOrientationVectors = 'Displ'
clip5Display.ScaleFactor = 2000.0
clip5Display.SelectScaleArray = 'Press_elem'
clip5Display.GlyphType = 'Arrow'
clip5Display.GlyphTableIndexArray = 'Press_elem'
clip5Display.GaussianRadius = 100.0
clip5Display.SetScaleArray = ['POINTS', 'Displ']
clip5Display.ScaleTransferFunction = 'PiecewiseFunction'
clip5Display.OpacityArray = ['POINTS', 'Displ']
clip5Display.OpacityTransferFunction = 'PiecewiseFunction'
clip5Display.DataAxesGrid = 'GridAxesRepresentation'
clip5Display.SelectionCellLabelFontFile = ''
clip5Display.SelectionPointLabelFontFile = ''
clip5Display.PolarAxes = 'PolarAxesRepresentation'
clip5Display.ScalarOpacityFunction = press_elemPWF
clip5Display.ScalarOpacityUnitDistance = 85.8567900736086

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip5Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip5Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip5Display.DataAxesGrid.XTitleFontFile = ''
clip5Display.DataAxesGrid.YTitleFontFile = ''
clip5Display.DataAxesGrid.ZTitleFontFile = ''
clip5Display.DataAxesGrid.XLabelFontFile = ''
clip5Display.DataAxesGrid.YLabelFontFile = ''
clip5Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip5Display.PolarAxes.PolarAxisTitleFontFile = ''
clip5Display.PolarAxes.PolarAxisLabelFontFile = ''
clip5Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip5Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(clip4, renderView1)

# show color bar/color legend
clip5Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=clip5.ClipType)

renderView1.ResetCamera()

# get animation scene
animationScene1 = GetAnimationScene()

animationScene1.PlayMode = 'Sequence'

# Properties modified on animationScene1
animationScene1.NumberOfFrames = 200

# find source
clip5 = FindSource('Clip5')

# create a new 'Elevation'
elevation1 = Elevation(Input=clip5)
elevation1.LowPoint = [3950.0, 12336.0, 2805.0]
elevation1.HighPoint = [23950.0, 14104.734375, 22805.0]

# find source
xdmf3ReaderS1 = FindSource('Xdmf3ReaderS1')

# Properties modified on elevation1
elevation1.LowPoint = [13950.0, 12600.0, 12805.0]
elevation1.HighPoint = [13950.0, 14104.734375, 12805.0]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1803, 824]

# show data in view
elevation1Display = Show(elevation1, renderView1)

# get color transfer function/color map for 'Elevation'
elevationLUT = GetColorTransferFunction('Elevation')

# get opacity transfer function/opacity map for 'Elevation'
elevationPWF = GetOpacityTransferFunction('Elevation')

# trace defaults for the display properties.
elevation1Display.Representation = 'Surface'
elevation1Display.ColorArrayName = ['POINTS', 'Elevation']
elevation1Display.LookupTable = elevationLUT
elevation1Display.OSPRayScaleArray = 'Elevation'
elevation1Display.OSPRayScaleFunction = 'PiecewiseFunction'
elevation1Display.SelectOrientationVectors = 'Veloc'
elevation1Display.ScaleFactor = 2000.0
elevation1Display.SelectScaleArray = 'Elevation'
elevation1Display.GlyphType = 'Arrow'
elevation1Display.GlyphTableIndexArray = 'Elevation'
elevation1Display.GaussianRadius = 100.0
elevation1Display.SetScaleArray = ['POINTS', 'Elevation']
elevation1Display.ScaleTransferFunction = 'PiecewiseFunction'
elevation1Display.OpacityArray = ['POINTS', 'Elevation']
elevation1Display.OpacityTransferFunction = 'PiecewiseFunction'
elevation1Display.DataAxesGrid = 'GridAxesRepresentation'
elevation1Display.SelectionCellLabelFontFile = ''
elevation1Display.SelectionPointLabelFontFile = ''
elevation1Display.PolarAxes = 'PolarAxesRepresentation'
elevation1Display.ScalarOpacityFunction = elevationPWF
elevation1Display.ScalarOpacityUnitDistance = 519.2349192338299

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
elevation1Display.DataAxesGrid.XTitleFontFile = ''
elevation1Display.DataAxesGrid.YTitleFontFile = ''
elevation1Display.DataAxesGrid.ZTitleFontFile = ''
elevation1Display.DataAxesGrid.XLabelFontFile = ''
elevation1Display.DataAxesGrid.YLabelFontFile = ''
elevation1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
elevation1Display.PolarAxes.PolarAxisTitleFontFile = ''
elevation1Display.PolarAxes.PolarAxisLabelFontFile = ''
elevation1Display.PolarAxes.LastRadialAxisTextFontFile = ''
elevation1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(clip5, renderView1)

# show color bar/color legend
elevation1Display.SetScalarBarVisibility(renderView1, True)

# find source
clip3 = FindSource('Clip3')

# find source
clip2 = FindSource('Clip2')

# find source
clip1 = FindSource('Clip1')

# find source
clip4 = FindSource('Clip4')

# update the view to ensure updated data information
renderView1.Update()

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
elevationLUT.ApplyPreset('Linear Green (Gr4L)', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
elevationPWF.ApplyPreset('Linear Green (Gr4L)', True)

# set active source
SetActiveSource(clip5)

# show data in view
clip5Display = Show(clip5, renderView1)

# get color transfer function/color map for 'Press_elem'
press_elemLUT = GetColorTransferFunction('Press_elem')

# get opacity transfer function/opacity map for 'Press_elem'
press_elemPWF = GetOpacityTransferFunction('Press_elem')

# trace defaults for the display properties.
clip5Display.Representation = 'Surface'
clip5Display.ColorArrayName = ['CELLS', 'Press_elem']
clip5Display.LookupTable = press_elemLUT
clip5Display.OSPRayScaleArray = 'Displ'
clip5Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip5Display.SelectOrientationVectors = 'Displ'
clip5Display.ScaleFactor = 2000.0
clip5Display.SelectScaleArray = 'Press_elem'
clip5Display.GlyphType = 'Arrow'
clip5Display.GlyphTableIndexArray = 'Press_elem'
clip5Display.GaussianRadius = 100.0
clip5Display.SetScaleArray = ['POINTS', 'Displ']
clip5Display.ScaleTransferFunction = 'PiecewiseFunction'
clip5Display.OpacityArray = ['POINTS', 'Displ']
clip5Display.OpacityTransferFunction = 'PiecewiseFunction'
clip5Display.DataAxesGrid = 'GridAxesRepresentation'
clip5Display.SelectionCellLabelFontFile = ''
clip5Display.SelectionPointLabelFontFile = ''
clip5Display.PolarAxes = 'PolarAxesRepresentation'
clip5Display.ScalarOpacityFunction = press_elemPWF
clip5Display.ScalarOpacityUnitDistance = 85.8567900736086

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip5Display.DataAxesGrid.XTitleFontFile = ''
clip5Display.DataAxesGrid.YTitleFontFile = ''
clip5Display.DataAxesGrid.ZTitleFontFile = ''
clip5Display.DataAxesGrid.XLabelFontFile = ''
clip5Display.DataAxesGrid.YLabelFontFile = ''
clip5Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip5Display.PolarAxes.PolarAxisTitleFontFile = ''
clip5Display.PolarAxes.PolarAxisLabelFontFile = ''
clip5Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip5Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# show color bar/color legend
clip5Display.SetScalarBarVisibility(renderView1, True)

# set scalar coloring
ColorBy(clip5Display, ('POINTS', 'Veloc', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(press_elemLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
clip5Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
clip5Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Veloc'
velocLUT = GetColorTransferFunction('Veloc')

# Properties modified on velocLUT
velocLUT.EnableOpacityMapping = 1

# set active source
SetActiveSource(elevation1)

# create a new 'Threshold'
threshold1 = Threshold(Input=elevation1)
threshold1.Scalars = ['POINTS', 'Elevation']
threshold1.ThresholdRange = [0.0, 1.0]

# Properties modified on threshold1
threshold1.Scalars = ['CELLS', 'Mat']
threshold1.ThresholdRange = [0.0, 0.0]

# show data in view
threshold1Display = Show(threshold1, renderView1)

# trace defaults for the display properties.
threshold1Display.Representation = 'Surface'
threshold1Display.ColorArrayName = ['POINTS', 'Elevation']
threshold1Display.LookupTable = elevationLUT
threshold1Display.OSPRayScaleArray = 'Elevation'
threshold1Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1Display.SelectOrientationVectors = 'Veloc'
threshold1Display.ScaleFactor = 2000.0
threshold1Display.SelectScaleArray = 'Elevation'
threshold1Display.GlyphType = 'Arrow'
threshold1Display.GlyphTableIndexArray = 'Elevation'
threshold1Display.GaussianRadius = 100.0
threshold1Display.SetScaleArray = ['POINTS', 'Elevation']
threshold1Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1Display.OpacityArray = ['POINTS', 'Elevation']
threshold1Display.OpacityTransferFunction = 'PiecewiseFunction'
threshold1Display.DataAxesGrid = 'GridAxesRepresentation'
threshold1Display.SelectionCellLabelFontFile = ''
threshold1Display.SelectionPointLabelFontFile = ''
threshold1Display.PolarAxes = 'PolarAxesRepresentation'
threshold1Display.ScalarOpacityFunction = elevationPWF
threshold1Display.ScalarOpacityUnitDistance = 524.5539903626066

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
threshold1Display.DataAxesGrid.XTitleFontFile = ''
threshold1Display.DataAxesGrid.YTitleFontFile = ''
threshold1Display.DataAxesGrid.ZTitleFontFile = ''
threshold1Display.DataAxesGrid.XLabelFontFile = ''
threshold1Display.DataAxesGrid.YLabelFontFile = ''
threshold1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
threshold1Display.PolarAxes.PolarAxisTitleFontFile = ''
threshold1Display.PolarAxes.PolarAxisLabelFontFile = ''
threshold1Display.PolarAxes.LastRadialAxisTextFontFile = ''
threshold1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(elevation1, renderView1)

# show color bar/color legend
threshold1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(elevation1)

# set active source
SetActiveSource(threshold1)

# Properties modified on threshold1
threshold1.Input = clip5

# set active source
SetActiveSource(threshold1)

# set active source
SetActiveSource(elevation1)

# Properties modified on elevation1
elevation1.Input = threshold1

# set active source
SetActiveSource(elevation1)

# show data in view
elevation1Display = Show(elevation1, renderView1)

# show color bar/color legend
elevation1Display.SetScalarBarVisibility(renderView1, True)

# hide data in view
Hide(threshold1, renderView1)

# set active source
SetActiveSource(threshold1)

# rename source object
RenameSource('Select Ground', threshold1)

# set active source
SetActiveSource(clip5)

# rename source object
RenameSource('Keep relevant geometry', clip5)

# set active source
SetActiveSource(xdmf3ReaderS1)

# get display properties
xdmf3ReaderS1Display = GetDisplayProperties(xdmf3ReaderS1, view=renderView1)

# rename source object
RenameSource('Import mesh', xdmf3ReaderS1)

# rename source object
RenameSource('Import data', xdmf3ReaderS1)

# set active source
SetActiveSource(elevation1)

# rename source object
RenameSource('Elevation coloring', elevation1)

# set active source
SetActiveSource(clip5)

# create a new 'Threshold'
threshold1_1 = Threshold(Input=clip5)
threshold1_1.Scalars = None
threshold1_1.ThresholdRange = [-3.676100490679346e-08, 3.092142719651747e-08]

# set active source
SetActiveSource(threshold1)

# set active source
SetActiveSource(threshold1_1)

# Properties modified on threshold1_1
threshold1_1.Scalars = ['CELLS', 'Mat']
threshold1_1.ThresholdRange = [1.0, 1.0]

# show data in view
threshold1_1Display = Show(threshold1_1, renderView1)

# trace defaults for the display properties.
threshold1_1Display.Representation = 'Surface'
threshold1_1Display.ColorArrayName = None
threshold1_1Display.LookupTable = press_elemLUT
threshold1_1Display.OSPRayScaleArray = 'Veloc'
threshold1_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1_1Display.SelectOrientationVectors = 'Veloc'
threshold1_1Display.ScaleFactor = 21.0
threshold1_1Display.SelectScaleArray = 'Press_elem'
threshold1_1Display.GlyphType = 'Arrow'
threshold1_1Display.GlyphTableIndexArray = 'Press_elem'
threshold1_1Display.GaussianRadius = 1.05
threshold1_1Display.SetScaleArray = None
threshold1_1Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1_1Display.OpacityArray = ['POINTS', 'Veloc']
threshold1_1Display.OpacityTransferFunction = 'PiecewiseFunction'
threshold1_1Display.DataAxesGrid = 'GridAxesRepresentation'
threshold1_1Display.SelectionCellLabelFontFile = ''
threshold1_1Display.SelectionPointLabelFontFile = ''
threshold1_1Display.PolarAxes = 'PolarAxesRepresentation'
threshold1_1Display.ScalarOpacityFunction = press_elemPWF
threshold1_1Display.ScalarOpacityUnitDistance = 24.9731746358509

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
threshold1_1Display.ScaleTransferFunction.Points = [-4.5265227779430424e-29, 0.0, 0.5, 0.0, 1.5807215967936836e-29, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
threshold1_1Display.OpacityTransferFunction.Points = [-4.5265227779430424e-29, 0.0, 0.5, 0.0, 1.5807215967936836e-29, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
threshold1_1Display.DataAxesGrid.XTitleFontFile = ''
threshold1_1Display.DataAxesGrid.YTitleFontFile = ''
threshold1_1Display.DataAxesGrid.ZTitleFontFile = ''
threshold1_1Display.DataAxesGrid.XLabelFontFile = ''
threshold1_1Display.DataAxesGrid.YLabelFontFile = ''
threshold1_1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
threshold1_1Display.PolarAxes.PolarAxisTitleFontFile = ''
threshold1_1Display.PolarAxes.PolarAxisLabelFontFile = ''
threshold1_1Display.PolarAxes.LastRadialAxisTextFontFile = ''
threshold1_1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(clip5, renderView1)

# show color bar/color legend
threshold1_1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# rename source object
RenameSource('Select Dam', threshold1_1)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(press_elemLUT, renderView1)

# change solid color
threshold1_1Display.DiffuseColor = [0.6549019607843137, 0.6549019607843137, 0.6549019607843137]

# set active source
SetActiveSource(clip5)

# create a new 'Threshold'
threshold1_2 = Threshold(Input=clip5)
threshold1_2.Scalars = None
threshold1_2.ThresholdRange = [-3.676100490679346e-08, 3.092142719651747e-08]

# Properties modified on threshold1_2
threshold1_2.Scalars = ['CELLS', 'Mat']
threshold1_2.ThresholdRange = [2.0, 2.0]

# show data in view
threshold1_2Display = Show(threshold1_2, renderView1)

# trace defaults for the display properties.
threshold1_2Display.Representation = 'Surface'
threshold1_2Display.ColorArrayName = None
threshold1_2Display.LookupTable = press_elemLUT
threshold1_2Display.OSPRayScaleArray = 'Veloc'
threshold1_2Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1_2Display.SelectOrientationVectors = 'Veloc'
threshold1_2Display.ScaleFactor = 994.7335937500001
threshold1_2Display.SelectScaleArray = 'Press_elem'
threshold1_2Display.GlyphType = 'Arrow'
threshold1_2Display.GlyphTableIndexArray = 'Press_elem'
threshold1_2Display.GaussianRadius = 49.7366796875
threshold1_2Display.SetScaleArray = ['POINTS', 'Veloc']
threshold1_2Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1_2Display.OpacityArray = ['POINTS', 'Veloc']
threshold1_2Display.OpacityTransferFunction = 'PiecewiseFunction'
threshold1_2Display.DataAxesGrid = 'GridAxesRepresentation'
threshold1_2Display.SelectionCellLabelFontFile = ''
threshold1_2Display.SelectionPointLabelFontFile = ''
threshold1_2Display.PolarAxes = 'PolarAxesRepresentation'
threshold1_2Display.ScalarOpacityFunction = press_elemPWF
threshold1_2Display.ScalarOpacityUnitDistance = 643.4060825967855

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
threshold1_2Display.ScaleTransferFunction.Points = [-2.9448944364700246e-23, 0.0, 0.5, 0.0, 6.426354390187104e-23, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
threshold1_2Display.OpacityTransferFunction.Points = [-2.9448944364700246e-23, 0.0, 0.5, 0.0, 6.426354390187104e-23, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
threshold1_2Display.DataAxesGrid.XTitleFontFile = ''
threshold1_2Display.DataAxesGrid.YTitleFontFile = ''
threshold1_2Display.DataAxesGrid.ZTitleFontFile = ''
threshold1_2Display.DataAxesGrid.XLabelFontFile = ''
threshold1_2Display.DataAxesGrid.YLabelFontFile = ''
threshold1_2Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
threshold1_2Display.PolarAxes.PolarAxisTitleFontFile = ''
threshold1_2Display.PolarAxes.PolarAxisLabelFontFile = ''
threshold1_2Display.PolarAxes.LastRadialAxisTextFontFile = ''
threshold1_2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(clip5, renderView1)

# show color bar/color legend
threshold1_2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# rename source object
RenameSource('Select Water', threshold1_2)

# Properties modified on threshold1_2Display
threshold1_2Display.Opacity = 0.8

# Properties modified on threshold1_2Display
threshold1_2Display.Specular = 0.59

# Properties modified on threshold1_2Display
threshold1_2Display.Specular = 0.5

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(press_elemLUT, renderView1)

# change solid color
threshold1_2Display.DiffuseColor = [0.3333333333333333, 0.3333333333333333, 1.0]

# find source
keeprelevantgeometry = FindSource('Keep relevant geometry')

# set active source
SetActiveSource(keeprelevantgeometry)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1050, 824]

# show data in view
keeprelevantgeometryDisplay = Show(keeprelevantgeometry, renderView1)

# get color transfer function/color map for 'Veloc'
velocLUT = GetColorTransferFunction('Veloc')

# get opacity transfer function/opacity map for 'Veloc'
velocPWF = GetOpacityTransferFunction('Veloc')

# trace defaults for the display properties.
keeprelevantgeometryDisplay.Representation = 'Surface'
keeprelevantgeometryDisplay.ColorArrayName = ['POINTS', 'Veloc']
keeprelevantgeometryDisplay.LookupTable = velocLUT
keeprelevantgeometryDisplay.OSPRayScaleArray = 'Displ'
keeprelevantgeometryDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
keeprelevantgeometryDisplay.SelectOrientationVectors = 'Displ'
keeprelevantgeometryDisplay.ScaleFactor = 2000.0
keeprelevantgeometryDisplay.SelectScaleArray = 'Press_elem'
keeprelevantgeometryDisplay.GlyphType = 'Arrow'
keeprelevantgeometryDisplay.GlyphTableIndexArray = 'Press_elem'
keeprelevantgeometryDisplay.GaussianRadius = 100.0
keeprelevantgeometryDisplay.SetScaleArray = ['POINTS', 'Displ']
keeprelevantgeometryDisplay.ScaleTransferFunction = 'PiecewiseFunction'
keeprelevantgeometryDisplay.OpacityArray = ['POINTS', 'Displ']
keeprelevantgeometryDisplay.OpacityTransferFunction = 'PiecewiseFunction'
keeprelevantgeometryDisplay.DataAxesGrid = 'GridAxesRepresentation'
keeprelevantgeometryDisplay.SelectionCellLabelFontFile = ''
keeprelevantgeometryDisplay.SelectionPointLabelFontFile = ''
keeprelevantgeometryDisplay.PolarAxes = 'PolarAxesRepresentation'
keeprelevantgeometryDisplay.ScalarOpacityFunction = velocPWF
keeprelevantgeometryDisplay.ScalarOpacityUnitDistance = 85.8567900736086

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
keeprelevantgeometryDisplay.DataAxesGrid.XTitleFontFile = ''
keeprelevantgeometryDisplay.DataAxesGrid.YTitleFontFile = ''
keeprelevantgeometryDisplay.DataAxesGrid.ZTitleFontFile = ''
keeprelevantgeometryDisplay.DataAxesGrid.XLabelFontFile = ''
keeprelevantgeometryDisplay.DataAxesGrid.YLabelFontFile = ''
keeprelevantgeometryDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
keeprelevantgeometryDisplay.PolarAxes.PolarAxisTitleFontFile = ''
keeprelevantgeometryDisplay.PolarAxes.PolarAxisLabelFontFile = ''
keeprelevantgeometryDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
keeprelevantgeometryDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# show color bar/color legend
keeprelevantgeometryDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Veloc'
velocLUT = GetColorTransferFunction('Veloc')

# Rescale transfer function
velocLUT.RescaleTransferFunction(0.0, 7e-14)

# get opacity transfer function/opacity map for 'Veloc'
velocPWF = GetOpacityTransferFunction('Veloc')

# Rescale transfer function
velocPWF.RescaleTransferFunction(0.0, 7e-14)

# find source
clip2 = FindSource('Clip2')

# find source
elevationcoloring = FindSource('Elevation coloring')

# find source
selectDam = FindSource('Select Dam')

# find source
clip3 = FindSource('Clip3')

# find source
selectWater = FindSource('Select Water')

# find source
importdata = FindSource('Import data')

# find source
clip4 = FindSource('Clip4')

# find source
clip1 = FindSource('Clip1')

# find source
selectGround = FindSource('Select Ground')


# get camera animation track for the view
cameraAnimationCue1 = GetCameraTrack(view=renderView1)

# create a key frame
keyFrame10070 = CameraKeyFrame()
keyFrame10070.Position = [15167.231920578499, 19238.65654633237, 22094.586342120772]
keyFrame10070.FocalPoint = DAM_POS
keyFrame10070.ViewUp = [-0.0045746043082910415, 0.9253351550608452, -0.3791225709502721]
keyFrame10070.ParallelScale = 14169.760242231576
keyFrame10070.PositionPathPoints = [
    15167.25705589535, 20000, 22094.734422526715,
    14264.745793204836, 18500, 20145.352921633665,
    13975.405275160723, 12707, 13242.28309097738,
]
keyFrame10070.FocalPathPoints = DAM_POS
keyFrame10070.ClosedPositionPath = 0

# create a key frame
keyFrame10071 = CameraKeyFrame()
keyFrame10071.KeyTime = 0.5
keyFrame10071.Position = 13975.405275160723, 12707.069791239914, 13242.28309097738,
keyFrame10071.FocalPoint = DAM_POS
keyFrame10071.ViewUp = [-0.0045746043082910415, 0.9253351550608452, -0.3791225709502721]
keyFrame10071.ParallelScale = 14169.760242231576


# initialize the animation track
cameraAnimationCue1.Mode = 'Path-based'
cameraAnimationCue1.KeyFrames = [keyFrame10070, keyFrame10071]

# animationScene1.Play()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [34640.44666888083, 43114.68649436659, 46740.55142638823]
renderView1.CameraFocalPoint = [13949.99999999995, 12546.642578125027, 12804.999999999965]
renderView1.CameraViewUp = [-0.24367420440485832, 0.7898112474020101, -0.5628686130749698]
renderView1.CameraParallelScale = 19000.28458824738

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

path = '.'
for x in range(20):
    filename = path+'/image_'+str(x).ljust(4, 0)+'.png'
    SaveScreenshot(filename, magnification=3, quality=100, view=renderView1)
    animationScene1.GoToNext()
