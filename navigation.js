
(() => {
    const pages = [
        {
            file: "index.html",
            name: "Simulation",
            icon: "🧪"
        },
        {
            file: "tutorial.html",
            name: "Tutorial",
            icon: "📖"
        },
        {
            file: "about.html",
            name: "About",
            icon: "ℹ️"
        },
        {
            file: "references.html",
            name: "References",
            icon: "📚"
        },
        {
            file: "credits.html",
            name: "Credits",
            icon: "👥"
        },
        {
            file: "disclaimer.html",
            name: "Disclaimer",
            icon: "⚠️"
        }
    ];

    const currentPage =
        location.pathname.split("/").pop() || "index.html";

    const toggle = document.createElement("button");
    toggle.id = "site-nav-toggle";
    toggle.type = "button";
    toggle.setAttribute("aria-label", "Open navigation");
    toggle.setAttribute("aria-expanded", "false");
    toggle.textContent = "☰";

    const backdrop = document.createElement("div");
    backdrop.id = "site-nav-backdrop";

    const nav = document.createElement("nav");
    nav.id = "site-nav";
    nav.setAttribute("aria-label", "Main navigation");

    const links = pages.map(page => {
        const active = currentPage === page.file;

        return `
            <a href="${page.file}"
               class="${active ? "active" : ""}"
               ${active ? 'aria-current="page"' : ""}>
                <span class="nav-icon">${page.icon}</span>
                <span>${page.name}</span>
            </a>
        `;
    }).join("");

    nav.innerHTML = `
        <div class="site-nav-brand">
            <div class="site-nav-logo">⌁</div>
            <div>
                <div class="site-nav-title">THERMODYNAMICS LAB</div>
                <div class="site-nav-subtitle">Interactive Learning Environment</div>
            </div>
        </div>

        <div class="site-nav-label">Project Navigation</div>

        <div class="site-nav-links">
            ${links}
        </div>

        <div class="site-nav-footer">
            Thermodynamics Lab 3D<br>
            Academic Year 2026–2027
        </div>
    `;

    function openMenu() {
        nav.classList.add("open");
        backdrop.classList.add("open");
        document.body.classList.add("nav-open");

        toggle.textContent = "✕";
        toggle.setAttribute("aria-expanded", "true");
        toggle.setAttribute("aria-label", "Close navigation");
    }

    function closeMenu() {
        nav.classList.remove("open");
        backdrop.classList.remove("open");
        document.body.classList.remove("nav-open");

        toggle.textContent = "☰";
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation");
    }

    toggle.addEventListener("click", () => {
        if (nav.classList.contains("open")) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    backdrop.addEventListener("click", closeMenu);

    document.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            closeMenu();
        }
    });

    nav.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", closeMenu);
    });

    document.body.append(toggle, backdrop, nav);
})();
