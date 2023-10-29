import React from 'react';
import "./getupdate.css"
import {Link} from "react-router-dom"

const Getupdate = () => {
    return (
        <div className='get-updates-cont'>
            <h1 className='d-flex justify-content-center m-2'>Update the food orders here</h1>

            {/* for processsing btn */}
            <div class="container1">
             

                <a href='#/process-order' class="button type--A">
                    <div class="button__line"></div>
                    <div class="button__line"></div>
                    <span class="button__text">Update Processing order</span>
                    <div class="button__drow1"></div>
                    <div class="button__drow2"></div>
                </a>
                <a href="#/dispatch-order" class="button type--B">
                    <div class="button__line"></div>
                    <div class="button__line"></div>
                    <span class="button__text">Update dispatch order</span>
                    <div class="button__drow1"></div>
                    <div class="button__drow2"></div>
                </a>
                <a href="#/ontheway-order" class="button type--C">
                    <div class="button__line"></div>
                    <div class="button__line"></div>
                    <span class="button__text">Update on the way</span>
                    <div class="button__drow1"></div>
                    <div class="button__drow2"></div>
                </a>
                <a href="#/delivered-order" class="button type--D">
                    <div class="button__line"></div>
                    <div class="button__line"></div>
                    <span class="button__text">Get delivered order</span>
                    <div class="button__drow1"></div>
                    <div class="button__drow2"></div>
                </a>
            </div>
        </div>
    );
}

export default Getupdate;
