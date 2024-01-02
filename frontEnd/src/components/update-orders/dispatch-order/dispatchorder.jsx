import React, { useEffect, useState } from 'react';
import "./dispatchorder.css"

const Dispatchorder = () => {
    const [data, setdata] = useState([]);
    const [orderid, setorderid] = useState(0);
    const [status, setStatus] = useState('Select the status');

    useEffect(() => {
        fetch('http://localhost:9999/dispatch-order')
            .then(res => res.json())
            .then(data => {
                console.log(data);
                setdata(data);
            })
            .catch(err => console.log(err));
    }, [])



    function handleupdate_status() {
        let stat_data = {
            order_id: orderid,
            status: status,
        }

        fetch('http://localhost:9999/update-order-req', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(stat_data)

        }).then(res => res.json())
            .then(data => {
                if (data.message == "success") {
                    location.reload();
                }
                else {
                    console.log("techincal issues");
                }
            })

    }


    return (
        <div className='dis-home justify-content-center'>
            <h1>Update the Dispatch order here</h1>
            <h5>The dispatch orders are</h5>
            <div className='dis-h'>
                {
                    data.length > 0 && data.map((o, i) => (


                        <div key={i}>
                            <p>{o.order_id},</p>
                        </div>


                    ))
                }
            </div>
            <div>
                <h5> Select the order id and status of the order
                </h5>

                <select onChange={e => setorderid(e.target.value)}>
                    <option key={0} value={0}>order id</option>
                    {
                        data.map((o, i) => (
                            <option key={o.order_id} value={o.order_id}>{o.order_id}</option>
                        ))
                    }
                </select>
                <p>{orderid}</p>
            </div>
            <div>
                <select onChange={e => setStatus(e.target.value)}>
                    <option value={null}>Select the status</option>
                    <option key={1} value='Your order is out for delivery'>Your order is out for delivery</option>
                    <option key={2} value='your order has been delivered successfully'>your order has been delivered successfully</option>
                </select>
            </div>
            <p>{status}</p>

            <button className='btn btn-primary' onClick={handleupdate_status}>Update</button>
        </div>
    );
}

export default Dispatchorder;
