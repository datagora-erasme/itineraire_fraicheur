
import React from 'react';
import Map from '../components/map'

import Content from '../components/content';
import BackButton from '../components/backButton';

function Home(){
    return (
        <div style={{position: 'relative'}} className="min-h-screen max-h-screen">
            <BackButton/>
            <Content/>
            <Map/>
        
        </div>
    );
}

export default Home; 