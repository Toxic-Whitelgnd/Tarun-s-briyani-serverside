const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const db = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'1234',
    database:'tarun_briyani'

})



app.get('/inprogress',(req,res) => {
    const query1 = "select * from order_tracking where status ='Your order is in prepration';";

    db.query(query1,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
});

app.get('/dispatchorder',(req, res)=>{
    const q = "select * from order_tracking where status = 'Your order is ready yet to dispatch';";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
    
});

app.get('/onthewayorder',(req, res)=>{
    const q = "select * from order_tracking where status = 'Your order is out for delivery';";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
    
});

app.get('/get-deliverd-order',(req, res)=>{
    const q = "select * from order_tracking where status = 'your order has been delivered successfully';";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
    
});

app.post('/update-orders',(req,res) => {
    let{order_id,status} = req.body;
    console.log(order_id,status);

    // db query 
    
    const q = "update order_tracking set status = '"+status+"' where order_id = '"+order_id+"' ";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
    })

    return res.json({"message":"success"})
});

app.get('/',(req,res)=>{
    res.json("Server for Tarun's Briyani paradise ");
}
);

app.listen(9999,()=>{
    console.log("listening on port:http://localhost:9999");
})