;(function () {
  const originalWindowInit = Mirador.Window.prototype.init

  const template = Mirador.Handlebars.compile(
    [
      '<select class="{{selectClassName}}" style="margin-right: 5px;">',
      '{{#canvases}}',
      '<option value="{{id}}">{{label}}</option>',
      '{{/canvases}}',
      '</select>',
    ].join('')
  )

  Mirador.Window.prototype.init = function () {
    const windowObj = this

    originalWindowInit.apply(windowObj)

    const canvases = windowObj.imagesList.map(function (canvas) {
      canvas.id = canvas['@id']
      return canvas
    })

    windowObj.element.find('.window-manifest-navigation').prepend(
      template({
        selectClassName: 'page-select',
        canvases,
      })
    )

    windowObj.element.find('.page-select').on('change', function (event) {
      const canvasID = jQuery(this).val()
      windowObj.eventEmitter.publish(
        'SET_CURRENT_CANVAS_ID.' + windowObj.id,
        canvasID
      )
    })
  }
})()
