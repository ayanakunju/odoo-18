/** @odoo-module */
import { WebsitePublicComponent } from '@website/components/public_component_wrapper';
import { registry } from '@web/core/registry';
import PublicWidget from "@web/legacy/js/public/public_widget"


// Extend WebsitePublicComponent instead of PublicWidget
export const themeIndex = PublicWidget.Widget.extend({
    setup() {
        super.setup();
        this.selector = "#wrapwrap";
        this.counters = null;
    }

    // Updated event handling for Odoo 18
    events() {
        return {
            'scroll': '_handleScroll',
        };
    }

    async start() {
        await super.start();
        this.counters = this.el;
        // Add scroll event listener
        window.addEventListener('scroll', this._handleScroll.bind(this));
    }

    // Method to handle the scroll event
    _handleScroll() {
        const counters = this.el.querySelectorAll('.number');
        const speed = 1000; // Define the speed for counting animation

        const animateCounters = () => {
            // Iterate over each counter element
            counters.forEach((counter) => {
                const updateCount = () => {
                    const target = +counter.getAttribute("data-target");
                    const count = +counter.innerText;
                    const increment = target / speed;

                    if (count < target) {
                        counter.innerText = Math.ceil(count + increment);
                        setTimeout(updateCount, 200);
                    } else {
                        counter.innerText = target;
                    }
                };
                updateCount(); // Call the 'updateCount' function to start the counting animation
            });
        };

        // Get the current scroll position plus the window height
        const scrollPosition = window.scrollY + window.innerHeight;

        counters.forEach((counter) => {
            const counterPosition = counter.offsetTop + counter.clientHeight / 2;
            if (scrollPosition >= counterPosition) {
                animateCounters();
            }
        });
    }

    destroy() {
        // Clean up event listener when component is destroyed
        window.removeEventListener('scroll', this._handleScroll.bind(this));
        super.destroy();
    }
})

// Register the component in the public components registry
 PublicWidget.registry.themeIndex = themeIndex






//




///** @odoo-module */
//import PublicWidget from "@web/legacy/js/public/public_widget"
//// Extend the PublicWidget.Widget class to create a new widget for the theme
//export const themeIndex = PublicWidget.Widget.extend({
//// Set the selector to the element with id 'wrapwrap', which is the main container of the page
//    // Define the events to be handled by the widget
//    setup(){
//    this.counters= null;
//    console.log('222222222222',this.counters)
//    }
//
//    events: {
//        'scroll': '_handleScroll',
//    },
//    // The 'start' method is a when the widget is initialized
//    async start(){
//    await super.start();
//        this.counters = this.el;
//    },
//    // Method to handle the scroll event
//    _handleScroll() {
//        var counters = this.el.querySelectorAll('.number')
//        const speed = 1000;// Define the speed for counting animation
//
//
//      const animateCounters = () => {
//        // Iterate over each counter element
//        counters.each((key,counter) => {
//          const updateCount = () => {
//            const target = +(counter).getAttribute("data-target");
//            const count = +(counter).innerText;
//            const increment = target / speed;
//
//            if (count < target) {
//              counter.innerText = Math.ceil(count + increment);
//              setTimeout(updateCount, 200);
//            } else {
//                counter.innerText = target;
//                       }
//          };
//
//          updateCount();// Call the 'updateCount' function to start the counting animation
//        });
//      };
//    // Get the current scroll position plus the window height
//    const scrollPosition = window.scrollY + window.innerHeight;
//    counters.each((key,counter) => {
//      const counterPosition = counter.offsetTop + counter.clientHeight / 2;
//      if (scrollPosition >= counterPosition) {
//        animateCounters();
//      }
//    });
//    },
// })
// // Register the widget so it can be used on the website
// PublicWidget.registry.themeIndex = themeIndex












///** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget"
// Define a new widget called NavigationScroll
export const NavigationScroll = PublicWidget.Widget.extend({
    setup() {
        super.setup();
        this.selector = "#wrapwrap";
    }

    events() {
        return {
            'scroll': '_handleScroll',
        };
    }

    async start() {
        await super.start();
        this._handleNavStyle();
        this._navbar_animation();
        this._hero_animation();

        const actionManager = document.querySelector('.homepage');

        // Video Animation
        gsap.fromTo(
            ".anime_video",
            { x: "-100vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".anime_video",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    once: true,
                }
            }
        );

        gsap.fromTo(
            ".anime_video_right",
            { x: "200vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".anime_video_right",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    once: true,
                }
            }
        );

        // Service Animation
        gsap.fromTo(
            ".anime_h",
            {
                y: "-100%",
                opacity: 0,
            },
            {
                y: 0,
                opacity: 1,
                duration: 2,
                ease: "power3.out",
                delay: 0.5,
                scrollTrigger: {
                    trigger: ".anime_h",
                    start: "top 50%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    once: true,
                },
            }
        );

        // Cards Animation
        gsap.from(".anime_card", {
            opacity: 0,
            y: 100,
            duration: 1.2,
            ease: "power3.out",
            stagger: {
                each: 0.3,
                from: "start",
            },
            scrollTrigger: {
                trigger: ".anime_grid",
                start: "top 50%",
                toggleActions: "play none none none",
                scroller: actionManager,
                once: true,
            },
        });

        // Process Animation
        gsap.fromTo(
            ".anime_h2",
            { x: "-100vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".anime_h2",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    invalidateOnRefresh: true,
                    once: true,
                }
            }
        );

        gsap.fromTo(
            ".anime_card2",
            { x: "200vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".anime_card2",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    invalidateOnRefresh: true,
                    once: true,
                }
            }
        );

        gsap.fromTo(
            ".anime_grid2",
            { x: "200vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".anime_grid2",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    invalidateOnRefresh: true,
                    once: true,
                }
            }
        );

        // Testimonial Animation
        gsap.fromTo(
            ".testimonial",
            { x: "-100vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".testimonial",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    invalidateOnRefresh: true,
                    once: true,
                }
            }
        );

        // Location Animation
        gsap.fromTo(
            ".location_head",
            { x: "-100vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".location_head",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    invalidateOnRefresh: true,
                    once: true,
                }
            }
        );

        gsap.fromTo(
            ".location_left",
            { x: "-100vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".location_left",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    invalidateOnRefresh: true,
                    once: true,
                }
            }
        );

        gsap.fromTo(
            ".location_right",
            { x: "200vw", opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 1.5,
                scrollTrigger: {
                    trigger: ".location_right",
                    start: "top 80%",
                    toggleActions: "play none none none",
                    scroller: actionManager,
                    invalidateOnRefresh: true,
                    once: true,
                }
            }
        );
    }

    _handleNavStyle() {
        const currentPath = window.location.pathname;
        const targetNav = this.el.querySelectorAll('a.nav-link');
        const logoName = this.el.querySelector('#theme_name');
        const toggleButton = this.el.querySelector('.navbar-toggler img');

        if (currentPath === "/") {
            if (targetNav.length > 0) {
                targetNav.forEach(nav => nav.classList.remove('nav-link2'));
                logoName.classList.add('span1');
                logoName.classList.remove('brandD');
            }
        } else {
            if (targetNav.length > 0) {
                targetNav.forEach(nav => nav.classList.add('nav-link2'));
                logoName.classList.add('brandD');
                logoName.classList.remove('span1');
                if (toggleButton) {
                    toggleButton.setAttribute('src', '/theme_upshift/static/src/img/icons/black.svg');
                }
            }
        }
    }

    _navbar_animation() {
        const timeline = gsap.timeline({ default: { duration: 1 } });
        timeline
            .from(".navigation", { y: "-100%", duration: 2, ease: "bounce" })
            .from(".nav-link", { opacity: 0, stagger: 0.5 })
            .from(
                ".navbar-brand",
                { x: "-100%", opacity: 0 },
                { x: "0%", opacity: 1, ease: "power1.in" },
                "<.5"
            );
    }

    _hero_animation() {
        const letters = document.querySelectorAll(".text span");

        gsap.to(letters, {
            opacity: 1,
            y: 0,
            duration: 0.5,
            ease: "power2.out",
            stagger: 0.1,
        });

        gsap.registerPlugin();

        class RevealOnLoad {
            constructor() {
                this.DOM = {
                    hero: document.querySelector(".hero"),
                    hero_title: document.querySelector(".hero__title"),
                    hero_subtitle: document.querySelector(".hero__subtitle"),
                };
                this.tl = gsap.timeline();
                this.init();
            }

            init() {
                this.tl.add(this.heroAnimation());
            }

            heroAnimation() {
                var tl = gsap.timeline({ defaults: { duration: 1, opacity: 0 } });
                tl.from(this.DOM.hero, {
                    scale: 2,
                });
                tl.from(this.DOM.hero_title, {
                    y: -10,
                    scale: 0.5,
                });
                tl.from(this.DOM.hero_subtitle, {
                    y: 10,
                    scale: 0.5,
                });
                return tl;
            }
        }
        new RevealOnLoad();
    },

    _handleScroll() {
        const currentPath = window.location.pathname;
        const navigation = this.el.querySelector(".navigation");

        if (window.scrollY > 0) {
            if (currentPath === "/") {
                navigation.classList.add("scrolled");
            } else {
                navigation.classList.add("scrolled2");
            }
        } else {
            navigation.classList.remove("scrolled", "scrolled2");
        }
    },
});

PublicWidget.registry.NavigationScroll = NavigationScroll;
