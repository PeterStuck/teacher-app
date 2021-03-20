gsap.timeline()
    .from('#time_spared', {duration: 1.5, opacity: 0, ease: "back.out(1.7)"})
    .from('#time_spared_label', {duration: 0.5, opacity: 0})
    .from('.available_apps a', {opacity: 0, yPercent: 200, stagger: {amount: 0.5}, ease: "power3.out"})