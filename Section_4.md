# Building a Shopping Cart API:

# Designing the API:
	- First define what operations do we need to support.

	- REQUEST TYPE         ENDPOINT              REQUSET BODY            RESPONSE BODY
	
	- Create a Cart                                 POST /create 200
	- Add Items to Create							POST /add-item -  
	- Update quantity of items						PATCH /update -cartitem_item, quantity
	- Remove item from create						PATCH /delete-item  item_id
	- Get a cart with all its items					GET /cart-item -cart-id
	- Delete a Cart 								POST /delete

	- Creating a Cart:   POST   /carts/  {}       cart
	- Body of the request is empty here because our carts are anonymous.
	- We do NOT want to force user to login before they can item to their shopping cart.
	- When creating a cart we are not going to send someone's user_id or customer_id to get a cart back.
	- We send a POST request to "/carts/" endpoint and we get a cart object back from server.
	- This cart object has a unique identifier that we will save.

	- Getting a Cart :       GET     /carts/:id      {}    cart

	- Deleting a Cart :       DELETE     /carts/:id      {}    {}

	- Adding item to Cart:    POST       /carts/:id/items       {prodID, qty}          item
	- This endpoint represents for a particular cart. 
	- In request body we are only sending "product_id" and "qua ntity" and the cart_id will be get from the url.
	- In response we will get an item object.
	- This item also has an unique identifier which we will use later.


	- Updating a Cart:        PATCH      /carts/:id/items/:id         {qty}           {qty}
	- Here we have 2 url parameters, first one is "cart_id" 2nd is "cartItem_id".
	- We will send quantity in the request body and get the updated quantity back as a response
	- We will support only "patch" request not "put" requests.
	- Because with "put" we will have to replace an entire object. And here we only want to update the quantity. So therefore we will use "patch" request only
	
	- Deleting a Item:       DELETE     /carts/:id/items/:id         {}           {}



	- /carts/                     CartViewSet
	- /carts/:id                  CartViewSet
 
	- /carts/:id/items            CartItemViewSet
	- /carts/:id/items/:id        CartItemViewSet



# Revisiting our data model:
	Our current Cart and CartItem are:

	class Cart(models.Model):
    	created_at = models.DateTimeField(auto_now_add=True)

	class CartItem(models.Model):
    	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    	product = models.ForeignKey(Product, on_delete=models.CASCADE)
    	quantity = models.PositiveSmallIntegerField()

    - Django automatically gives each model a primary key field.
    - And that primary_field will be an integer and this integer field can easily be guessed by any hacker.
    - Hacker can easily guess someone else's Cart_id and can mess with that cart by sending a request to this endpoint
    - To solve this problem, we will use "GUID: Globally Unique Identifier"
    - It is a long 32-character string. It will be much harder to guess.
    - so, we will redefine primary_key field.

    from uuid import uuid4

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    - Here in default value we are NOT calling "uuid4" , we are just passing a reference to it.
    - If we call the function here then, at the time we create a migration a "GUID" will be generated and will be hardcoded in our migration file.
    - So, we should NOT call thsis method here.

    - Right now in our database, the primary_key of "cart" is a "bigint" filed which is of size 8 bytes.
    - If we cinvert this to GUID, we will be storig 32 bytes. (3 times larger field size)
    - And we are also storing this id in "CartItem" table.

    - Some people are totally against using "GUID" because they take a lot of spaces and performance wise they are a bit slower than integers.
    - But lets do the assesment,
    - Lets say we will have a 1 million enteries in our carts.
    
    - For 1 million enteries, we are stroing additional 24 bytes.
    - 1000000 x 24 = 24000000 B
    - 24000000/1024 = 23437.5 kB
    - 23437.5/1024 = 22.8 MBs

    - These days 22 MB is not a big issue anymore. (For 1 million users)
    - Also, And as people place orders, we will move these records to our "Order" and "OrderItem" table. Ans in those table we will NOT use "GUID"
    
    - Because the Order's API, that we will build later, is gonna be secure.
    - It will not be open to an anynomous user.
    - A client has to authenticate and authorize to access a particular order.
    - So we will use GUID

    - Also, in "Cart" table, we have a field called "created_at" and with this we can keep track of abando carts.
    - So, if some people, add some items to the shopping cart and then forget about it, every now and then we can clean this table.
    - We can run a script and remove every "cart" which is, lets say, 3 months older.
    - So this table, will NOT grow quiet large.

    - So, in theory, looking up a GUID key is slower than an Integer-key.
    - But these days, our services are so powerful and also all this database engines are highly optimized.
    - So we do NOT need to do any optimization here before doing a proper test.

    - "PREMATURE OPTIMIZATION IS THE ROOT OF ALL EVIL  - Donald Knuth"

    - ALTERNATIVE SOLUTION:
    	- Keep the table as is .i.e., leave the primary_key as an integer field
    	- Add an additional column and we can call ir "unique_id" and in that column we will store a "GUID"
    	- With this change, we will not be saving "GUID" in "CartItem" table "Cart" as a foriegn_key
    	- There, we will only have integers.
    	- And now each cart has a "GUID", in our APIs instead of a number we can use that "GUID"
    	- And internally we will translate that "GUID" to a number.
    	- This will complicate our queries a very much.

    - So, we will use previous approach.

    - In CartItem make a following change:

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    - This means our cart item will have a foriegn key field with the name of 'items'

	- At the moment we can add same products multiple time in one cart. This is not the bahaviour we want.
	- If the user adds same product more than one time, intead of adding it multiple times, we will just increase the quantity of that product.
	- Using a unique constraint, we can make sure that there are no duplicate records for the same product in the same cart.

	- For that we wiil add Meta class, here we will have list of lists where we can define unique constarint for multiple fields.

	class Meta:
        unique_together = [['cart', 'product']]

    - Apply these chnages:

    python manage.py makemigrations
    python manage.py migrate


