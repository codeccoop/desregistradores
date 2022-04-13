import {Link} from "react-router-dom";
import { useRef } from "react";


function Header() {

    function onBurgerClick (ev) {
        ev.preventDefault();
        $burger.current.classList.toggle("is-active");
        $menu.current.classList.toggle("is-active");
    }

    const $burger = useRef(null);
    const $menu = useRef(null);

    return (
        <header className="header">  
            <nav className="navbar" role="navigation" aria-label="main navigation">
                <div className="navbar-brand">
                    <Link className="navbar-item" to="/">
                        <p className="title is-5">Desregistradores</p>
                    </Link>
                    <a
                        role="button"
                        className="navbar-burger"
                        aria-label="menu"
                        aria-expanded="false"
                        href="/"
                        ref={$burger}
                        onClick={onBurgerClick}
                    >
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                    </a>
                </div>
                <div
                    className="navbar-menu"
                    ref={$menu}
                >
                    <div className="navbar-start">
                        <Link
                            className="navbar-item"
                            to="/about"
                        >
                            Sobre el projecte
                        </Link>
                    </div>
                </div>
            </nav>
        </header>
    );
  }
  
  export default Header;