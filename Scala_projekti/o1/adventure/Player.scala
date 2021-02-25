package o1.adventure

import scala.collection.mutable.Map


/** A `Player` object represents a player character controlled by the real-life user of the program.
  *
  * A player object's state is mutable: the player's location and possessions can change, for instance.
  *
  * @param startingArea  the initial location of the player */
class Player(startingArea: Area) {

  private var currentLocation: Area = startingArea        // gatherer: changes in relation to the previous location
 
  private var quitCommandGiven: Boolean = false              // one-way flag
  
  private val items: Map[String, Item] = Map[String, Item]()
  
  //Checks if player has the item
  
  def  has(itemName: String): Boolean = this.items.contains(itemName)
  
  //Removes item from player
  
  def removeItem(itemName: String): Option[Item] = {
    this.items.remove(itemName)
  }
  
  // Calls safes method open
  
  def open(modifiers: String): String = {
    val splitted = modifiers.split(' ')
    if(this.location == safe.location.get){
    safe.open(splitted(splitted.size - 1))
    }else "You have to be in same room with the safe to open it"
  }
  
  // Calls items method use if player is carrying the item or if item belongs to BigItems and is in same location.
  
  def use(itemName: String): String = {
    if(this.has(itemName)){
      this.items(itemName).use
    }else if(this.currentLocation.contains(itemName) && !this.currentLocation.items(itemName).canPickUp){
      this.location.items(itemName).use
    }else "You can't use " + itemName + ". \nYou should first pick it up or get close to it and remember that you can't do things with everything."
  }
  
  //Picks up item if it belongs to SmallItems
  
  def get(itemName: String): String = {
    if(this.location.contains(itemName)){
      if(this.location.items(itemName).canPickUp){
        this.location.items(itemName).pickedUp(this)
        this.items += (itemName -> this.location.removeItem(itemName).get)
        "You pick up the " + itemName + "."
      }else "The " + itemName + " is too big for you to pick up."
    }else "There is no " + itemName + " here to pick up."
  }
  
  //Drops item if player is carrying it
  
  def drop(itemName: String): String = {
    if(this.has(itemName)){
      this.items(itemName).dropped
      this.location.addItem(this.items.remove(itemName).get)
      "You drop the " + itemName + "." 
    }else "You don't have that!"
  }
  
  //Returns the description of item if player is carrying it
  
  def  examine(itemName: String): String = {
    if(this.has(itemName)) {
      "You look closely at the " + itemName + ".\n" + this.items(itemName).description
    }else "If you want to examine something, you need to pick it up first."
  }
  
  //Returns the description of item if player is in same location than it and it belongs to BigItems
  
  def lookAt(modifiers: String): String = {
    val itemName = modifiers.dropWhile(_ != ' ').trim
    if(this.currentLocation.contains(itemName)){
      if(this.currentLocation.items(itemName).canPickUp){
        "The " + itemName + " is too small to examine this far. \nPick it first up and examine it after that"
      }else "You look at the " + itemName + ". \n" + this.currentLocation.items(itemName).description
    }else if(this.has(itemName)) "You should try to examine it rather than look at it."
    else "You can't look at something you dont have in your sight."
  }
  
  //Returns names of the items, player is carrying
  
  def  inventory: String = {
    if(this.items.size > 0){
       "You are carrying\n" + this.items.keys.mkString("\n")
    }else "You are empty-handed."
  }


  /** Determines if the player has indicated a desire to quit the game. */
  def hasQuit: Boolean = this.quitCommandGiven


  /** Returns the current location of the player. */
  def location: Area = this.currentLocation


  //Attempts to move player to given direction.
  //Is successful if there is exit in given direction and dog isn't blocking the way
  //While moving updates the locations of players items
  
  def go(direction: String): String = {
    val destination = this.location.neighbor(direction)
    if(destination.isDefined){
      if(destination.get.name == "Bedroom" || destination.get.name == "Workroom"){
        if(dog.isInTheWay == false){
          this.currentLocation = destination.get
          this.items.values.foreach(_.location = Some(this.location))
          "You go " + direction + "."
        }else "You can't go " + direction + ", because the dog is in blocking the way."
      }else {
        this.currentLocation = destination.get
        this.items.values.foreach(_.location = Some(this.location))
        "You go " + direction + "."
      }
    }else "You can't go " + direction + "."
  }


  /** Causes the player to rest for a short while (this has no substantial effect in game terms).
    * Returns a description of what happened. */
  def rest(): String = {
    "You rest for a while. Better get a move on, though."
  }


  /** Signals that the player wants to quit the game. Returns a description of what happened within
    * the game as a result (which is the empty string, in this case). */
  def quit(): String = {
    this.quitCommandGiven = true
    ""
  }


  /** Returns a brief description of the player's state, for debugging purposes. */
  override def toString = "Now at: " + this.location.name


}


