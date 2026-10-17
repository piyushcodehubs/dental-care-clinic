
document.addEventListener("DOMContentLoaded", function () {
    const revealElements = document.querySelectorAll(".reveal");

    // Fallback for browsers without IntersectionObserver.
    if (!("IntersectionObserver" in window)) {
        revealElements.forEach(function (element) {
            element.classList.add("visible");
        });
        return;
    }

    const observer = new IntersectionObserver(
        function (entries, currentObserver) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    currentObserver.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.12,
            rootMargin: "0px 0px -35px 0px"
        }
    );

    revealElements.forEach(function (element, index) {
        // Small stagger for a smoother entrance.
        element.style.transitionDelay = (index % 3) * 100 + "ms";
        observer.observe(element);
    });
});








document.addEventListener("DOMContentLoaded", function () {

    // Scroll reveal animations
    const revealElements = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.15 }
        );

        revealElements.forEach(function (element) {
            revealObserver.observe(element);
        });
    } else {
        revealElements.forEach(function (element) {
            element.classList.add("visible");
        });
    }

    // Animated statistics counters
    const counters = document.querySelectorAll(".counter");
    const duration = 2000;

    function animateCounter(counter) {
        if (counter.dataset.animated === "true") return;
        counter.dataset.animated = "true";

        const target = Number(counter.dataset.target);
        const suffix = counter.dataset.suffix || "";
        const isShortFormat = counter.dataset.format === "short";
        const startTime = performance.now();

        function updateCounter(currentTime) {
            const progress = Math.min(
                (currentTime - startTime) / duration,
                1
            );

            // Smooth ease-out effect
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            const value = Math.floor(
                1 + (target - 1) * easedProgress
            );

            if (progress >= 1) {
                counter.textContent =
                    (isShortFormat
                        ? (target / 1000) + "K"
                        : target) + suffix;
                return;
            }

            counter.textContent = isShortFormat
                ? (value >= 1000
                    ? (value / 1000).toFixed(1).replace(/\.0$/, "") + "K"
                    : value)
                : value;

            requestAnimationFrame(updateCounter);
        }

        requestAnimationFrame(updateCounter);
    }

    // Start counting when statistics become visible
    const statsSection = document.querySelector(".home-stats");

    if (statsSection && "IntersectionObserver" in window) {
        const statsObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        counters.forEach(animateCounter);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.25 }
        );

        statsObserver.observe(statsSection);
    } else {
        counters.forEach(animateCounter);
    }

});

