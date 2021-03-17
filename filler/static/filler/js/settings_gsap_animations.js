gsap.timeline()
    .from('.form_wrapper', {opacity: 0, y: 200, stagger: 0.5, ease: "back.out(1.7)"})
    .from('.alert', {opacity: 0})