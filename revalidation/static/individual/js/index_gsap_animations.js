gsap.timeline()
    .from('#flex_form', {duration: 0.7, y: 200, opacity: 0, ease: "circ.out"}, 'form')
    .from('.form__submit', {duration: 2, y: 200, opacity: 0, ease: "elastic.out(1, 0.3)"})
    .from('.settings_wrapper', {duration: 1, yPercent: 250, ease: "back.out(1.7)"})