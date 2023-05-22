
import React from 'react';
import Map from '../components/map'

import Content from '../components/content';

function Home(){
    return (
        <div style={{position: 'relative'}} className="min-h-screen max-h-screen">
            <Content/>
            <Map/>
        
        </div>
    );
}

export default Home; 