gsap.timeline()
    .add('main_content')
    .from('.filter_panel', { duration: 0.5, y: 200, opacity: 0, ease: "power1. out" }, 'main_content')
    .from('.saved_topics', { duration: 0.5, y: 200, opacity: 0, ease: "power1. out" }, 'main_content')
    .from('table', { duration: 0.5, opacity: 0, ease: "power1. out" })
    .from('.topic', { duration: 0.5, opacity: 0, stagger: 0.3, ease: "power1. out" })
    .from('.pagination', { duration: 0.5, opacity: 0, ease: "power1. out" });