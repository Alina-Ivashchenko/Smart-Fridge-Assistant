# Title: Smart Fridge Assistant
# Summary: 
The Smart Fridge Assistant is a comprehensive web application
designed to manage food inventory, track expiry dates, generate AI-based
recipe suggestions, and provide nutritional information for food items. Initially
proposed as a simple inventory tracking system, the project evolved
significantly, adding features like AI recipe generation, expiry tracking, ima
recognition for fridge contents, and nutritional analysis for better food
awareness and healthier meal planning.
# Key refinements include:
- AI-based Recipe Generator that uses inventory data to generate
personalized recipes.
- Ingredient Expiry Tracking to reduce food waste through timely
notification
- Nutritional Information Analysis that provides users with the nutritional
values (calories, protein, carbs, fats, etc.) of each ingredient or recipe.
These features improve user experience, automate kitchen tasks, and
promote healthier and more sustainable food usage.
# Back-End Integration
- Flask Routes: The Flask server handles different routes that allow users
to interact with the database through forms and user actions on the
front end.
+ For example, when a user submits a new inventory item, the
front-end sends a request to the Flask server, which processes the
data and updates the MySQL database.
Data Flow Example:
1. User Inputs Ingredient: The user adds a new item via main.html by
filling out a form (e.g., adding eggs to their fridge
2. Form Submission: The form sends an HTTP POST request to the Flask
back-end with the ingredient data.
3. Database Update: Flask processes the form data, constructs an SQL
query, and executes it against the MySQL database to update the Items
table.
4. Response to User: After the update, the front-end is refreshed or
updated dynamically to reflect the changes made to the inventor
No User Entity
Since there is no User entity in this system, all data is handled without user
authentication or profiles. The system interacts with the database witho
differentiating between individual users. All actions, such as inventory
management and recipe generation, are global and not personalized for any
specific use.
# Future Improvements
### 1. Advanced AI Recipe Customization
Users will be able to filter recipes by health goals (low-car
high-protein) and difficulty leve
### 2. Image Recognition
Implement image recognition to support more items and provide
nutritional data instantly after recognition.
### 3. Enhanced Nutritional Analysis
Meal Planner: Provide daily calorie tracking and personalized
nutrition plans for users.
Data Visualization: Visualize users' calorie and nutrition intake
trends using interactive dashboards.
### 4. Mobile App Integration
Scan & Track: A mobile app could let users scan barcodes to add
items directly to the inventory.
### 5. Offline Mode
Support for offline mode, with sync functionality wh
reconnected.
### 6. Voice Assistant Integration
Voice commands for adding items, requesting recipes, and
checking nutritional information.
