import { useState } from 'react'

import './App.css'
import React,{useEffect} from 'react'
import { HashRouter as Router, Route, Routes } from "react-router-dom";
import Homepage from './components/homepage/homepage';
import NavBar from './components/navbar/navbar';
import Getupdate from './components/getupdates/getupdate';
import Footer from './components/footer/footer';
import Processorder from './components/update-orders/processing-order/processorder';
import Dispatchorder from './components/update-orders/dispatch-order/dispatchorder';
import Ontheway from './components/update-orders/on-the-way/ontheway';
import Deliveredorder from './components/update-orders/deliverd-order/deliveredorder';

function App() {

  return (
    <>
      <div>
      <Router>
      <NavBar />
      <Routes>
      <Route path='/' index element={<Homepage />}/>
      <Route path='/getupdates' element={<Getupdate />} />
      <Route path='/process-order' element={<Processorder />} />
      <Route path='/dispatch-order' element={<Dispatchorder />} />
      <Route path='/ontheway-order' element={<Ontheway />} />
      <Route path='/delivered-order' element={<Deliveredorder />} />
      </Routes>
      <Footer />
    </Router>
      </div>
    </>
  )
}

export default App
