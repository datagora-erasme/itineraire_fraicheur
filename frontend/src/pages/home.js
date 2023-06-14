
import React from 'react';
import Map from '../components/map'

import Content from '../components/content';
import BackButton from '../components/backButton';
import HeadBand from '../components/headband';

function Home(){
    return (
        <div style={{position: 'relative'}} className="min-h-screen max-h-screen">
            {/* <HeadBand/> */}
            <BackButton/>
            <Content/>
            <Map/>
        
        </div>
    );
}

export default Home; 