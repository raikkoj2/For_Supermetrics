package o1.adventure


/** The class `Action` represents actions that a player may take in a text adventure game.
  * `Action` objects are constructed on the basis of textual commands and are, in effect,
  * parsers for such commands. An action object is immutable after creation.
  * @param input  a textual in-game command such as "go east" or "rest" */
class Action(input: String) {

  private val commandText = input.trim.toLowerCase
  
  private val verb        = commandText.takeWhile( _ != ' ' )
  
  private val modifiers   = commandText.drop(verb.length).trim
  
  private val extraModifier = modifiers.split(' ').head


  /** Causes the given player to take the action represented by this object, assuming
    * that the command was understood. Returns a description of what happened as a result
    * of the action (such as "You go west."). The description is returned in an `Option`
    * wrapper; if the command was not recognized, `None` is returned. */
  def execute(actor: Player) = this.verb match {
    case "go"        => Some(actor.go(this.modifiers))
    case "rest"      => Some(actor.rest())
    case "quit"      => Some(actor.quit())
    case "get"       => Some(actor.get(this.modifiers))
    case "drop"      => Some(actor.drop(this.modifiers))
    case "examine"   => Some(actor.examine(this.modifiers))
    case "inventory" => Some(actor.inventory)
    case "use"       => if(extraModifier == "safe") Some("Try to open safe.") else Some(actor.use(this.modifiers))
    case "open"      => if(extraModifier == "safe") Some(actor.open(this.modifiers)) else None
    case "look"      => if(extraModifier == "at") Some(actor.lookAt(this.modifiers)) else None
    case "help"      => Some(this.helpText)
    case other       => None
  }


  /** Returns a textual description of the action object, for debugging purposes. */
  override def toString = this.verb + " (modifiers: " + this.modifiers + ")"
  
  //Returns description of new commands added to the game.
  
  val helpText: String = {
    """You have some new commands you might need to use while playing the game.
    |use beef = You can feed a beef to something
    |use gun = You can shoot with the gun but after every shot your turns lower faster
    |use sedatives = You can drug  the beef you are carrying
    |examine "some item" = You can examine items you are carrying
    |look at "some item" = If item is too big to carry, you can examine it by looking at it
    |open safe "some password" = If password, you give, is correct, the safe opens""".stripMargin
  }


}

