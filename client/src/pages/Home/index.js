import {Link} from "react-router-dom";
import "./style.scss"

function Home() {
    return (
        <main className="home">  
            <nav className="home__buttons columns">
                <Link className="home__button column" to="/map"> Accedeix al mapa</Link>
                <Link className="home__button column" to="/form"> Afegeix una nota simple</Link>
                <Link className="home__button column" to="/download"> Descarrega les dades en format .csv</Link>
            </nav>
        </main>
    );
  }
  
  export default Home;