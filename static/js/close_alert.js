function close_alert(event) {
    gsap.to('.alert', {duration: 1 , xPercent: 100, opacity: 0})
    setTimeout(() => {
        document.querySelector('.alert').style.display = 'none';
    }, 1000)
}