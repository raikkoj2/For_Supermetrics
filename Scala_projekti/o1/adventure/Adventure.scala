package o1.adventure
import scala.math._


/** The class `Adventure` represents text adventure games. An adventure consists of a player and
  * a number of areas that make up the game world. It provides methods for playing the game one
  * turn at a time and for checking the state of the game.
  *
  * N.B. This version of the class has a lot of "hard-coded" information which pertain to a very
  * specific adventure game that involves a small trip through a twisted forest. All newly created
  * instances of class `Adventure` are identical to each other. To create other kinds of adventure
  * games, you will need to modify or replace the source code of this class. */
class Adventure {

  /** The title of the adventure game. */
  val title = "Theft"
  
 //Creating all areas

  private val hallway    = new Area("Hallway", "You are in the hallway of the house. \nThere is three doors and stairs in the end of the hallway.")
  private val wc         = new Area("WC", "You are in the toilet. \nThere is only one way in and one way out.")
  private val bathroom   = new Area("Bathroom", "It's the bathroom but now isn't time for a shower.")
  private val storage    = new Area("Storage", "You are in th storage.\nThere is so much stuff laying around.")
  private val kitchen    = new Area("Kitchen", "You are in the kitchen. \nMaybe there is something to eat but you don't have time for that.")
  private val livingroom = new Area("Livingroom", "The heart of the house, livingroom! \nYou should do something to that angry dog blocking your way")
  private val bedroom    = new Area("Bedroom", "You are in the bedroom but now isn't the time for a nap")
  private val workroom   = new Area("Workroom", "You are in the workroom. \nThis feels promising.")  
  private val out        = new Area("Out", "You are out of the house")
  private val destination = out
  
  //Setting neighbors for areas

     hallway.setNeighbors(Vector(                      "east" -> kitchen,   "south" -> out,     "west" -> storage,  "up" -> livingroom ))
          wc.setNeighbors(Vector("north" -> kitchen                                                                                    ))
    bathroom.setNeighbors(Vector(                                           "south" -> storage                                         ))
     storage.setNeighbors(Vector("north" -> bathroom,  "east" -> hallway                                                               ))
     kitchen.setNeighbors(Vector(                                           "south" -> wc,      "west" -> hallway                      ))
  livingroom.setNeighbors(Vector(                                           "south" -> bedroom, "west" -> workroom, "down" -> hallway  ))
     bedroom.setNeighbors(Vector("north" -> livingroom                                                                                 ))
    workroom.setNeighbors(Vector(                      "east" -> livingroom                                                            ))
  
  //Adding items to areas
    
  hallway.addItem(new Picture("small picture"))
  bathroom.addItem(drugs)
  storage.addItem(gun)
  kitchen.addItem(beef)
  kitchen.addItem(new Picture("big picture"))
  livingroom.addItem(dog)
  livingroom.addItem(new Picture("huge picture"))
  bedroom.addItem(new Picture("enormous picture"))
  workroom.addItem(new SmallItems("papers", "These are his dogs, Garfields, adoption papers."))
  workroom.addItem(safe)
  
  //Adds new item when called if safe is opened and evidenceAdded is still false
  
  private var evidenceAdded = false
  
  def addEvidence: Unit = {
    if(safe.isOpen && !this.evidenceAdded){
    workroom.addItem(new SmallItems("evidence", "Yuo have now all the evidence and you should run."))
    this.evidenceAdded = true
    }
  }
  
  /** The character that the player controls in the game. */
  val player = new Player(hallway)
  
 //The number of turns player can still use
  var turnsLeft = 40
  
  /** Determines if the adventure is complete, that is, if the player has won. */
  def isComplete = this.player.location == this.destination && this.player.has("evidence")

  /** Determines whether the player has won, lost, or quit, thereby ending the game. */
  def isOver = this.isComplete || this.player.hasQuit || this.turnsLeft == 0 || (this.player.location == this.destination && !this.player.has("evidence"))

  /** Returns a message that is to be displayed to the player at the beginning of the game. */
  def welcomeMessage = """You are in the house of your blackmailer.
                       |
                       |You should find all the evidence he has against you but you should hurry the alarm just went off.""".stripMargin


  /** Returns a message that is to be displayed to the player at the end of the game. The message
    * will be different depending on whether or not the player has completed their quest. */
  def goodbyeMessage = {
    if (this.isComplete)
      "You did it! You got the evidence you came for and didn't get caught. \nYou won!"
    else if(this.player.location == this.destination && !this.player.has("evidence"))
        "What are you doing? You fled without the evidence and now you are going to jail. \nGame over!"
    else if (this.turnsLeft == 0)
      "Oh shit! The police is here and there is nowhere you could run.\nGame over!"
    else  // game over due to player quitting
      "Quitter!"
  }


  /** Plays a turn by executing the given in-game command, such as "go west". Returns a textual
    * report of what happened, or an error message if the command was unknown. In the latter
    * case, no turns elapse. */
  def playTurn(command: String): String = {
    val action = new Action(command)
    val outcomeReport = action.execute(this.player)
    //Updates the amount of turns the player has and adds evidence if safe is opened
    if (outcomeReport.isDefined) {
      this.turnsLeft = max(this.turnsLeft - gun.shotsFired - 1, 0)
      this.addEvidence
    }
    outcomeReport.getOrElse("Unknown command: \"" + command + "\".")
  }


}
