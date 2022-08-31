document.querySelectorAll('.allow-tabs')
    .forEach(el => {
        el.addEventListener('keydown', e => {
            if (e.key == 'Tab') {
                e.preventDefault()
                let start = el.selectionStart
                el.value = `${el.value.substring(0, start)}\t${el.value.substring(el.selectionEnd)}`
                el.selectionStart = el.selectionEnd = start + 1
            }
        })
    })
