document.addEventListener("DOMContentLoaded", () => {

    // Reveal animation
    const elements = document.querySelectorAll(
        ".damage-card, .workflow-step, .scanner-card"
    );

    const observer = new IntersectionObserver(
        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("visible");

                }

            });

        },
        {
            threshold: 0.15
        }
    );


    elements.forEach((element) => {
        observer.observe(element);
    });


    // Mouse movement effect on scanner
    const scanner = document.querySelector(".scanner-card");

    if (scanner) {

        scanner.addEventListener("mousemove", (event) => {

            const rect = scanner.getBoundingClientRect();

            const x =
                (event.clientX - rect.left) / rect.width - 0.5;

            const y =
                (event.clientY - rect.top) / rect.height - 0.5;

            scanner.style.transform = `
                perspective(1000px)
                rotateY(${x * 3}deg)
                rotateX(${-y * 3}deg)
            `;

        });


        scanner.addEventListener("mouseleave", () => {

            scanner.style.transform = "";

        });

    }

});
