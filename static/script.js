document.getElementById('search').addEventListener('input', function() {
    let filter = this.value.toLowerCase();
    let updates = document.querySelectorAll('.update-item');

    updates.forEach(function(update) {
        let text = update.querySelector('p').innerText.toLowerCase();
        if (text.includes(filter)) {
            update.style.display = '';
        } else {
            update.style.display = 'none';
        }
    });
});
