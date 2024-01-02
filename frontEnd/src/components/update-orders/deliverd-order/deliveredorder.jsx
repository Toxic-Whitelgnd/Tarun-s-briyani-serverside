import React, { useEffect, useState } from 'react';
import "./deliveredorder.css"

const Deliveredorder = () => {
    const [data, setdata] = useState([]);

    useEffect(() => {
        fetch('http://localhost:9999/get-delivered-order')
            .then(res => res.json())
            .then(data => {
                console.log(data);
                setdata(data);
            })
            .catch(err => console.log(err));
    }, [])



    return (
        <div className='proc-home'>
            <h1>Displaying the deliverd orders</h1>
            <h5>delivered orders</h5>
            <div className='progress-h'>
                {
                    data.length > 0 && data.map((o, i) => (


                        <div key={i}>
                            <p>{o.order_id},</p>
                        </div>


                    ))
                }
            </div>
            
        </div>
    );
}

export default Deliveredorder;
