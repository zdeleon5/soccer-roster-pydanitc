from typing import Optional

from fastapi import FastAPI, Path, HTTPException

from player import Player, PlayerRequest

from starlette import status

app = FastAPI()

players: list[Player] = [
    Player(id=1, name="Lionel Messi", position="Forward", team="Inter Miami", year_born=1987),
    Player(id=2, name="Cristiano Ronaldo", position="Forward", team="Al Nassr", year_born=1985),
    Player(id=3, name="Neymar Jr", position="Forward", team="Al Hilal", year_born=1992),
    Player(id=4, name="Kevin De Bruyne", position="Midfielder", team="Manchester City", year_born=1991),
    Player(id=5, name="Virgil van Dijk", position="Defender", team="Liverpool", year_born=1991),
]

@app.get("/players", status_code=status.HTTP_200_OK)
async def get_players() -> Optional[list[Player]]:
    if len(players) == 0:
        return
    return players

@app.get("/players/{player_id}", status_code=status.HTTP_200_OK)
async def get_player_by_id(player_id: int = Path(gt=0)) -> Player:
    for player in players:
        if player.id == player_id:
            return player
    raise HTTPException(status_code=404, detail="Player not found")


@app.get("/players/year_born/{year_born}", status_code=status.HTTP_200_OK)
async def get_players_by_year_born(year_born: int) -> Optional[list[Player]]:
    temp_players = []
    for player in players:
        if player.year_born == year_born:
            temp_players.append(player)
    return temp_players


@app.post("/players", status_code=status.HTTP_201_CREATED)
async def create_player(new_player: PlayerRequest) -> Player:
    new_player.id = 1 if len(players) == 0 else players[-1].id + 1
    new_player = Player(**new_player.model_dump())
    players.append(new_player)
    print(type(new_player))
    return new_player

@app.put("/players/{player_id}", status_code=status.HTTP_200_OK)
async def update_player_by_id(player_id: int, updated_player: PlayerRequest) -> Optional[Player]:
    for player in players:
        if player.id == player_id:
            # Update the existing player's fields
            player.name = updated_player.name
            player.position = updated_player.position
            player.team = updated_player.team
            player.year_born = updated_player.year_born
            return player  # Return the modified player instance directly

    # Raise exception if no matching player is found
    raise HTTPException(status_code=404, detail="Player not found")
@app.delete("/players/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int = Path(gt=0)) -> None:
    for player in players:
        if player.id == player_id:
            players.remove(player)
    raise HTTPException(status_code=404, detail="Player not found")