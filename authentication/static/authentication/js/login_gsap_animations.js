gsap.timeline()
    .from('.form_wrapper', {duration: 0.7, opacity: 0, y: 200, ease: "power4.out"})
    .from('#login_logo', {duration: 1, opacity: 0, ease: "back.out(1.7)"})