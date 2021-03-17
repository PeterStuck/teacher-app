gsap.timeline()
    .from('.saved_topics', { duration: 0.5, y: 200, opacity: 0, ease: "power1. out" })
    .from('table', { duration: 0.5, opacity: 0, ease: "power1. out" })
    .from('.topic', { duration: 0.5, opacity: 0, stagger: 0.3, ease: "power1. out" })
    .from('.pagination', { duration: 0.5, opacity: 0, ease: "power1. out" });