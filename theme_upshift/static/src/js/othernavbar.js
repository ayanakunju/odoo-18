/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
// Define a new widget called NavigationScroll
import { registry } from "@web/core/registry";

export const NavigationScroll = PublicWidget.Widget.extend({
    // Set the selector to the element with id 'wrapwrap', which is the main wrapper of the page
    selector: "#wrapwrap",

    start() {
        this._super.apply(this, arguments);
        this._handleNavStyle();// Apply styling to the navigation bar based on the current page
        this._navbar_animation();// Initialize navbar animations
        this._hero_animation();// Initialize animations for the hero section
        this._setupScrollHandler();
        this._initializeAnimations();//Initialize the homepage animations
    },

    _setupScrollHandler() {
        this._onScroll = this._onScroll.bind(this);
        window.addEventListener('scroll', this._onScroll);

        // Create an IntersectionObserver to handle animations
        this._setupIntersectionObserver();
    },

    _setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1,
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    this._triggerAnimation(target);
                    // Unobserve after triggering to ensure it only happens once
                    this.observer.unobserve(target);
                }
            });
        }, options);

        // Observe all animated elements
        const animatedElements = document.querySelectorAll(
            '.anime_video, .anime_video_right, .anime_h, .anime_card, .anime_h2, ' +
            '.anime_card2, .anime_grid2, .testimonial, .location_head, ' +
            '.location_left, .location_right'
        );

        animatedElements.forEach(element => {
            this.observer.observe(element);
        });
    },

    _triggerAnimation(element) {
        const actionManager = document.querySelector('.homepage');

        // Define animation based on element class
        if (element.classList.contains('anime_video')) {
            gsap.fromTo(element,
                { x: "-100vw",
                 opacity: 0 },
                { x: 0,
                  opacity: 1,
                  duration: 1.5 }
            );
        }
        else if (element.classList.contains('anime_video_right')) {
            gsap.fromTo(element,
                { x: "200vw", opacity: 0 },
                { x: 0, opacity: 1, duration: 1.5 }
            );
        }
        else if (element.classList.contains('anime_h')) {
            gsap.fromTo(element,
                { y: "-100%", opacity: 0 },
                {
                    y: 0,
                    opacity: 1,
                    duration: 2,
                    ease: "power3.out", // Smooth easing for cards as well
                    delay: 0.5
                }
            );
        }
        // Add similar conditions for other animated elements
        else if (element.classList.contains('anime_h2') ||
                 element.classList.contains('anime_card')||
                 element.classList.contains('testimonial')||
                 element.classList.contains('location_head') ||
                 element.classList.contains('location_left')) {
            gsap.fromTo(element,
                { x: "-100vw",
                  opacity: 0 },
                { x: 0,
                  opacity: 1,
                  duration: 1.5
                }
            );
        }
        else if (element.classList.contains('anime_card2') ||
                 element.classList.contains('anime_grid2') ||
                 element.classList.contains('location_right')) {
            gsap.fromTo(element,
                { x: "200vw",
                  opacity: 0 },
                { x: 0,
                 opacity: 1,
                 duration: 1.5 }
            );
        }
    },

    destroy() {
        if (this.observer) {
            this.observer.disconnect();
        }
        window.removeEventListener('scroll', this._onScroll);
        this._super.apply(this, arguments);
    },

    _initializeAnimations() {
        // This is now just initial setup - actual animations are triggered by the IntersectionObserver
        gsap.registerPlugin();
    },

    _handleNavStyle() {
        const currentPath = window.location.pathname;
        const targetNav = this.$el.find('a.nav-link');
        const logoName = this.$el.find('#theme_name');
        const toggleButton = this.$el.find('.navbar-toggler img');

        if (currentPath === "/") {
            if (targetNav.length > 0) {
                targetNav.removeClass('nav-link2');
                logoName.addClass('span1').removeClass('brandD');
            }
        } else {
            if (targetNav.length > 0) {
                targetNav.addClass('nav-link2');
                logoName.addClass('brandD').removeClass('span1');
                toggleButton.attr('src', '/theme_upshift/static/src/img/icons/black.svg');
            }
        }
    },

    _navbar_animation() {
    //Navbar Animation
        const timeline = gsap.timeline({ default: { duration: 1 } });
        timeline
            .from(".navigation", { y: "-100%", duration: 2, ease: "bounce" })
            .from(".nav-link", { opacity: 0, stagger: 0.5 })
            .from(
                ".navbar-brand",
                { x: "-100%", opacity: 0 }, // Start state (opacity 0)
                { x: "0%", opacity: 1, ease: "power1.in" },// End state (opacity 1)
                "<.5"// Overlap with previous animation
            );
    },

    _hero_animation() {
        const letters = document.querySelectorAll(".text span");
         // Animate each letter with a staggered delay
        gsap.to(letters, {
            opacity: 1, // Fade in
            y: 0,// Move from -20px to 0
            duration: 0.5,// Animation duration for each letter
            ease: "power2.out", // Easing for smooth effect
            stagger: 0.1,// Delay between each letter
        });

        const heroElements = {
            hero: document.querySelector(".hero"),
            hero_title: document.querySelector(".hero__title"),
            hero_subtitle: document.querySelector(".hero__subtitle"),
        };

        const tl = gsap.timeline({ defaults: { duration: 1, opacity: 0 } });
        tl.from(heroElements.hero, {
            scale: 2
        })
          .from(heroElements.hero_title, {
            y: -10,
            scale: 0.5
           })
          .from(heroElements.hero_subtitle, {
            y: 10,
            scale: 0.5
           });
    },

    _onScroll() {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const currentPath = window.location.pathname;

        if (scrollTop > 0) {
            if (currentPath === "/") {
                this.$el.find(".navigation")[0].classList.add("scrolled");
            } else {
                this.$el.find(".navigation")[0].classList.add("scrolled2");
            }
        } else {
            this.$el.find(".navigation")[0].classList.remove("scrolled", "scrolled2");
        }
    },
});

PublicWidget.registry.NavigationScroll = NavigationScroll;
