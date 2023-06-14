
import React, {useState} from 'react';
import Map from '../components/map'

import Content from '../components/content';
import BackButton from '../components/backButton';
import HeadBand from '../components/headband';

function Home(){
    const [showMenu, setShowMenu] = useState(true)
    return (
        <div style={{position: 'relative'}} className="min-h-screen max-h-screen">
            {/* <HeadBand/> */}
            <BackButton showMenu={showMenu}/>
            <Content showMenu={showMenu} setShowMenu={setShowMenu}/>
            <Map/>
        
        </div>
    );
}

export default Home; 