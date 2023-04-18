import React from 'react';
import {Link} from 'react-router-dom';

function NavBar(){
    return (
        <div className="navBar">
            <h1 className="agroNetTitle">Itinéraires Fraîcheurs</h1>
            <div className="linksContainer">
                <Link to="/" className="links linksNavBar"> Home </Link>
            </div>
        </div>
    )
}

export default NavBar;