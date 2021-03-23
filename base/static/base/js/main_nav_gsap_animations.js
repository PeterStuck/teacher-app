gsap.timeline()
    .from('#time_spared', {duration: 1, opacity: 0, ease: "back.out(1.7)"})
    .from('#time_spared_label', {duration: 0.25, opacity: 0})
    .from('.available_apps .app', {opacity: 0, yPercent: 200, stagger: {amount: 0.25}, ease: "power3.out"})