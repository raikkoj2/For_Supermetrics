package o1.adventure

//The trait Item defines values, variables and methods that every item in game at least has
trait Item {
  
  var playerHas: Boolean = false
  
  var playerHolding: Option[Player] = None
  
  var location: Option[Area] = None
  
  val name: String
 
  var description: String
  
  var canPickUp:Boolean
  
  def use: String
  
  def lookAt: String
  
  def dropped: Unit
  
  def pickedUp(player: Player): Unit
  
  /** Returns a short textual representation of the item (its name, that is). */
  override def toString = this.name

}


//SmallItems are items that you can pick up in the game

class SmallItems(val name: String, var description: String) extends Item {
  
  var canPickUp: Boolean = true
  
  def use: String = ""
  
  def lookAt: String = "The " + name + " is too small . Pick it up to examine it."
  
  def pickedUp(player: Player): Unit = {
    this.playerHas = true
    this.playerHolding = Some(player)
  }
  
  def dropped: Unit = {
    this.playerHas = false
    this.playerHolding = None
  }
}


//BigItems are items that you can't pick up

class BigItems(val name: String, var description: String) extends Item {
  
  var canPickUp: Boolean = false
  
  def use: String = "You can't do anything with it."
   
  def lookAt: String = this.description 
  
  def dropped: Unit = this.playerHas = false
  
  def pickedUp(player: Player): Unit = this.playerHas = false
}


//Class picture is for all pictures in game

class Picture(name: String) extends BigItems(name, "It's a nice picture of the owners dog.") {}


//Safe is an object and it belongs to BigItems

object safe extends BigItems("safe","It's an old safe and you need the right password to open it."){
 
  private var closed: Boolean = true
  
  def isOpen: Boolean = !this.closed
  
  //Method open opens the safe if player gives right password
  
  def open(password: String): String = {
    if(this.closed){
      if(password.toUpperCase == "GARFIELD") {
        closed = false
        "You have opened the safe!"
      }else "Wrong password!"
    }else "What the heck are you doing? The safe is already open!"
  }
}


//Dog is an object and belongs to BigItems. It can be alive or dead and awake or sleeping.

object dog extends BigItems("dog", "It's a big and agry dog. It looks like it want's to eat you."){
  
  private var alive: Boolean = true
  
  private var awaken: Boolean = true
  
  def isSleeping: Boolean = !this.awaken
  
  def isAlive: Boolean = this.alive
  
  //Tells if dog is blocking player from moving to workroom and livingroom
  
  def isInTheWay: Boolean = {
    if(this.alive == false || this.awaken == false) false else true
  }
  
  //Defines dogs locations description again when it's called
  
  private def changeLocationDescription: Unit ={
    this.location.get.description = "The heart of the house, livingroom! \nNow that you have dealt with the dog you may enter workroom and bedroom."
  }
  
  //Kills dog and changes it's description
  
  def kill: Unit = {
    this.alive = false
    this.changeLocationDescription
    this.description = "It's a corpse of a dog."
  }
  
  //Makes the dog sleep and changes it's description
  //You don't need here to take care of feeding sleeping dog because beef can be used only once
  
  def sleep: Unit = {
    this.awaken = false
    this.changeLocationDescription
    this.description = "It's a big dog but it's also quite cute while sleeping."
  }
}


//Gun is an object and belongs to SmallItems. It can be used to shoot.

object gun extends SmallItems("gun","It's a handgun loaded with 6 bullets.") {
  
  private var roundsLeft: Int = 6
  
  //The gun fires once and lowers it's ammo and updates it's description
  
  def shoot: Unit = {
    this.roundsLeft -= 1
    this.description = "It's a handgun loaded with " + this.roundsLeft + " bullets."
  }
  
  //Use calls method shoot and if dog is in the same room as player it also kills the dog
  
  override def use: String = {
    if(this.playerHas && this.location == dog.location && this.roundsLeft > 0){
      if(dog.isAlive){
        this.shoot
        dog.kill
        "You have killed the dog, but someone might have heard that and police might be coming faster."
      }else {
        this.shoot
        "You can't kill dog twice so don't waste your ammo and by the way the police is coming faster."    
      }
    }else if(this.roundsLeft > 0){
      this.shoot
      "Someone might have heard that and police might be coming faster."
    }else "You are out of ammo."
  }
  
  //Defines how many shots you have fired and is used to reduce the amount of turns you have
  def shotsFired: Int = 6 - this.roundsLeft
}


//Beef is an object and belongs to SmallItems. It can be feed to a dog.

object beef extends SmallItems("beef", "It's a big delicious piece of meat."){
  
  private var drugged: Boolean = false
  
  def isDrugged: Boolean = this.drugged
  
  // Makes beef drugged and changes it's description
  
  def drug: Unit = {
    this.drugged = true
    this.description = "It's a big piece of meat but there is something added to it."
  }
  
  //Feeds the beef to dog if its in same room and makes dog sleep if beef is drugged. Also removes beef from game.
  
  override def use: String = {
    if(this.location == dog.location && dog.isAlive){
      if(this.drugged){
        dog.sleep
        this.playerHolding.get.removeItem(this.name)
        "The dog ate the beef and is now sleeping."
      }else {
        this.playerHolding.get.removeItem(this.name)
        "The dog ate the beef but it's still in your way and angry."
      }
    }else if(this.location == dog.location) "A dead dog can't eat."
    else "You don't want to eat that. Try to find a dog and feed it to it."
  }
}


//Drugs (sedatives) is an object and belongs to SmallItems and can be used to drug the beef

object drugs extends SmallItems("sedatives", "It's a small ammount of sedatives that you could use to drug something."){
  
  //Use calls beefs method drug if player has beef and drugs and then removes drugs from game if beef got drugged.
  
  override def use = {
    if(beef.playerHas){
      beef.drug
      this.playerHolding.get.removeItem(this.name)
      "You have drugged the beef."
    }else "You should try to drug something eatable."
  }
}