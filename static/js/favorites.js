for (let star of document.querySelectorAll('.favorite'))
{
    if(!star.is_favorite_button) {
        star.is_favorite_button = true
        star.addEventListener('click', e => {
            fetch(star.href)
                .then(res => res.json())
                .then(data => {
                    star.children[data.favorited + 0].classList.remove('hidden')
                    star.children[1 - data.favorited].classList.add('hidden')
                })
            e.preventDefault()
        })
    }
}
