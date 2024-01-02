from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse

import db_helper
import generic_helper
import db_mongodb

global order_total
global order_id

app = FastAPI()
# to handle the orders
inprogress_orders = {}
inprogress_userdetails = {}

@app.post('/')
async def webhook_handler(request: Request):
    payload = await request.json()

    #After getting the payload resonse let us extract
    intent = payload["queryResult"]["intent"]["displayName"]
    parameter = payload["queryResult"]["parameters"]
    output_context = payload["queryResult"]["outputContexts"]
    session_id = generic_helper.extract_session_id(output_context[0]['name'])


    handle_intent_req = {
        'track.order context:ongoing-order': track_orderid,
        'order.add - context:ongoing-order': add_order,
        'order.remove - context: ongoing-order': remove_order,
        'order.complete context: ongoing-order': complete_order,
        'order.cancel context:ongoing order': cancel_order,
        'user.name':get_user_name,
        'user.mobno context:ongoing-details':get_user_mobileno,
        'user.address context:ongoing-details':get_user_address,
        # 'user.change context:ongoing-details':change_user_Details,
        'change name mob address':change_user_Details,
    }

    return handle_intent_req[intent](parameter, session_id)

def get_user_address(parameter,session_id):
    zipcode = parameter['zip-code']
    address = parameter['street-address'][0]['street-address']
    city  = parameter['street-address'][0]['city']
    busadd = parameter['street-address'][0]['business-name']


    print(zipcode)
    print(address)
    print(city + busadd)

    user_add = ''

    user_add+=address
    user_add+=busadd
    user_add+=', '+city
    user_add+=', '+zipcode

    print(user_add)


    if session_id not in inprogress_userdetails:
        fulfilment_text = "Please Enter your name and then come to mobile number"
    else:
        inprogress_userdetails[session_id].update({'address':user_add})

    name = inprogress_userdetails[session_id]['name']
    mob = inprogress_userdetails[session_id]['mobileno']
    address = inprogress_userdetails[session_id]['address']

    print(name, mob, address)

    print(inprogress_userdetails)
    if session_id not in inprogress_orders:
        fulfilment_text = "I am having trouble finding your order id!! please make the order again!"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfilment_text = "Sorry unfortunately I cant place the order due to server error"
        else:
            order_total = db_mongodb.get_total_order(order_id)
            fulfilment_text = f"Thank you for your information! Here is your order id#{order_id}" \
                              f"And your total is {order_total}" \
                              f"your food will be delivered shortly" \
                              f"Review your details here {name}," \
                              f"{mob},{address}" \
                              f"You can change the details here by saying " \
                              f"CHANGE <Wrong Name> to <correct name>,pass your name to CHANGE MOBILENO=, CHANGE ADDRESS=" \
                              f"if no you can say CONTINUE [Feature Not usable]" \


        del inprogress_orders[session_id]
        #review changes to the user details if they want to change then keyword is "change details"

        db_mongodb.save_user_details(inprogress_userdetails[session_id],order_id)

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })

def change_user_Details(parameter,session_id):
    try:
        old_name = parameter['person'][0]
        new_name = parameter['person'][1]
    except:
        old_name = parameter['person']

    mobnumber = parameter['number']
    address = parameter['street-address']
    zip_code = parameter['zip-code']

    fulfilment_text = "Default response"

    print(old_name , new_name , mobnumber , address , zip_code)

    # get the orderid by using the name parameter
    curr_orderid = int(db_mongodb.get_order_id(old_name))
    print(curr_orderid)

    if session_id not in inprogress_userdetails:
        inprogress_userdetails[session_id]= {'name':new_name['name']}
    
    
    
    print(mobnumber)
    if(mobnumber != ''):
        inprogress_userdetails[session_id].update({'mobileno':mobnumber})

    if(len(address) != 0):
        saddress = address['street-address']
        city  = address['city']
        busadd = address['business-name']
            
        user_add = ''

        user_add+=saddress
        user_add+=busadd
        user_add+=', '+city
        user_add+=', '+zip_code

        print(user_add)
        inprogress_userdetails[session_id].update({'address': user_add})

        res = db_mongodb.update_user_details(inprogress_userdetails[session_id], curr_orderid)
        if(res == "Updated successfully"):
            fulfilment_text = f"Successfully Changed your Details {inprogress_userdetails}" \
                                "How would You like to pay?"\
                                "1. Cash on delivery " \
                                "2. Credit card "\
                                "3. Upi option " \
                                "4. Debit card " \
                                "5. Net banking" \
                                
        else:
            fulfilment_text = "Failed due to some technical error"
    
    # for updating the name only
    if(mobnumber == '' and len(address) == 0):
        res = db_mongodb.update_name_field(inprogress_userdetails[session_id]['name'],curr_orderid)
        if(res == "Updated successfully"):
            fulfilment_text = f"Successfully Changed the username" \
                                "How would You like to pay?"\
                                "1. Cash on delivery " \
                                "2. Credit card "\
                                "3. Upi option " \
                                "4. Debit card " \
                                "5. Net banking" 
                                
        else:
            fulfilment_text = "Failed due to some technical error"

    print(fulfilment_text)

    # for updating the name and mobileno
    if(mobnumber != '' and len(address) == 0):
        res = db_mongodb.update_nameAndmob_field(inprogress_userdetails[session_id],curr_orderid)
        if(res == "Updated successfully"):
            fulfilment_text = f"Successfully Changed the username and mobile number."\
                                "How would You like to pay?"\
                                "1. Cash on delivery " \
                                "2. Credit card "\
                                "3. Upi option " \
                                "4. Debit card " \
                                "5. Net banking" \
                               
        else:
            fulfilment_text = "Failed due to some technical error"


    del inprogress_userdetails[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })


def get_user_mobileno(parameter,session_id):
    mobilno = parameter['number']

    if session_id not in inprogress_userdetails:
        fulfilment_text = "Please Enter your name and then come to mobile number"
    else:
        inprogress_userdetails[session_id].update({'mobileno':str(mobilno)})

    fulfilment_text = "Thank you for providing your phone number. Could you additionally provide me your delivery address!"

    print(inprogress_userdetails)

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })


def get_user_name(parameter,session_id):

    username = parameter['person']

    if session_id not in inprogress_userdetails:
        inprogress_userdetails[session_id] = username

    fulfilment_text = "Thank you for providing your Name. Could you additionally provide me your Phone Number!"

    print(inprogress_userdetails)

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })



def track_orderid(parameter,session_id):
    orderid = parameter['number']
    print(int(orderid))
    # the database call has been processed here
    order_status = db_mongodb.get_order_status(int(orderid))


    if order_status:
        if (order_status == "Your order is out for delivery"):
        #get the delivery boi details
            deliverdetails = db_mongodb.get_delivery_boy()
            fullfilment_text = f"Your order id #{orderid} is  {order_status} is " \
                               f"Deliverying by {deliverdetails[0]} and his contact number {deliverdetails[1]}"
        else:
            fullfilment_text = f"Your order id #{orderid} is  {order_status}"
    else:
        fullfilment_text = f"No order found ;["


    return JSONResponse(content={
        "fulfillmentText":fullfilment_text
    })


def add_order(parameter,session_id):
    food_items = parameter['food-item']
    quantity = parameter['number']

    new_food_dict = dict(zip(food_items,quantity))

    if session_id in inprogress_orders:
        #if it is already there then update to the current dict
        curr_food_dict = inprogress_orders[session_id]
        curr_food_dict.update(new_food_dict)
        inprogress_orders[session_id] = curr_food_dict

    else:
        inprogress_orders[session_id] = new_food_dict

    # extract it to str
    orders = generic_helper.extract_str(inprogress_orders[session_id])
    if len(food_items) != len(quantity):
        fulfilment_text = "Sorry I cant understand the food item and quantity can u specify it again!!"
    else:
        fulfilment_text = f"So far you have {orders} in your cart, Anything else or you can say cancel order to cancel your current order?"

    print("*******************")
    print(inprogress_orders)
    print("*******************")

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })

def remove_order(parameter,session_id):

    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "Please make some orders!!"
        })

    foods_items = parameter['food-item'] #items to be removed
    current_order = inprogress_orders[session_id] #contains the current itemsets

    not_foodorder = []
    removed_order = []

    for fooditem in foods_items:
        if fooditem not in current_order:
            not_foodorder.append(fooditem)
        else:
            removed_order.append(fooditem)
            del current_order[fooditem]

    if len(removed_order) > 0:
        fulfilment_text = f"Removed {','.join(removed_order)} from your cart"
    if len(not_foodorder) > 0:
        fulfilment_text = f"Your current order does not have {','.join(not_foodorder)}"

    if len(current_order.keys()) == 0:
        fulfilment_text = "Your cart is empty"
    else:
        order_str = generic_helper.extract_str(current_order)
        fulfilment_text = f"Here is what left in your cart {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })

def cancel_order(parameter,session_id):


    food_dict = inprogress_orders[session_id]
    print("$$$$$$$$$$$$$$$$$")
    print(food_dict)
    if(len(food_dict.keys()) > 0):
        for fi,q in food_dict.items():
            del food_dict[fi]

    fulfilment_text = "Your order has been successfully removed"

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })

def complete_order(parameter,session_id):
    if session_id not in inprogress_orders:
        fulfilment_text = "I am having trouble finding your order id!! please make the order again!"
    else:
        fulfilment_text = "Your order has been successfully placed " \
                             f"could you provide me your name? or you" \
                              f"can cancel order here!"
    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })


# iMPORTANT PART TO SAVING THE ORDER IN db
def save_to_db(order: dict):
    # get the new order id
    nxt_order_id = db_mongodb.get_next_orderid()

    fi = []
    qt = []

    # extracting one item and pushing to db
    for fooditems,quantity in order.items():

        fi.append(fooditems)
        qt.append(quantity)

    print(fi,qt,nxt_order_id)

    rcode = db_mongodb.create_orders(
        fi,
        qt,
        nxt_order_id
    )

    if rcode == -1:
        return -1


    return nxt_order_id



# f"you can say CHANGE details or else no! \n" \
#                               "we can proceed with payment option" '\n' \
#                               "1. Cash on delivery \n" \
#                               "2. Credit card \n" \
#                               "3. Upi option \n" \
#                               "4. Debit card \n" \
#                               "5. Net banking \n" \