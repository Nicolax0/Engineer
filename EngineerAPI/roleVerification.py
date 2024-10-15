import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


    
def generate_random_code():
    random.randint(100000, 999999)

# add functionality to check if RCSID is already in database
def send_verification_code(RCSID):
    email = RCSID + "@rpi.edu"    
    message = MIMEMultipart()
    message['From'] = os.getenv("GMAIL")
    message['To'] = email
    message["Subject"] = "Verification Code"
    
    verificationCode = generate_random_code

    message.attach(MIMEText("Your code is: {verificationCode}. Please DM the Engineer bot this code. You have 15 minutes and 5 attempts." , "plain"))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.getenv("GMAIL"), os.getenv("GMAIL_PASS"))
        server.sendmail(os.getenv("GMAIL"), email, message.as_string())

        print(f"Email successfully sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    finally:
        try:
            server.quit()
        except Exception as quit_error:
            print(f"Failed to close the connection properly: {quit_error}")
    return True

@bot.command(name='verify')
async def ping(ctx, RCSID: str):
    userID = ctx.author.id
    code = send_verification_code(RCSID)
    if code is not None:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE discord_id = %s", (userID,))
            result = cursor.fetchone()
            if result: 
                cursor.execute("UPDATE users SET rcs_id = %s, correct_code = %s, attempts = 0 WHERE discord_id = %s",
                    (RCSID, code, userID))
            else:
                # Insert new user
                cursor.execute("INSERT INTO users (discord_id, rcs_id, correct_code, attempts) VALUES (%s, %s, %s, 0)",
                    (userID, RCSID, code))
            conn.commit()
        except Exception as db_error:
            print(f"Database error: {db_error}")
            await ctx.send("An error occurred while accessing the database.")
        finally:
            cursor.close()
            conn.close()
        try:
            await ctx.author.send(
                f"Hello! A verification code has been sent to your RPI email ({RCSID}@rpi.edu). "
                "Please reply to this message with the code to complete verification."
            )
            await ctx.send("A verification code has been sent to your RPI email. Please check your DMs.")
        except discord.Forbidden:
            await ctx.send(
                "I was unable to send you a DM. Please adjust your privacy settings to receive DMs from server members."
            )
    else:
        await ctx.send("Failed to send verification email. Please try again later.")

@bot.event
async def on_message(message):
    # Ensure the bot doesn't process its own messages
    if message.author == bot.user:
        return

    # Check if the message is a DM to the bot
    if isinstance(message.channel, discord.DMChannel):
        userID = message.author.id
        # Get the user from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT correct_code, attempts FROM users WHERE discord_id = %s", (userID,))
            result = cursor.fetchone()
            if result:
                correct_code, attempts = result
                if correct_code is None:
                    await message.channel.send("You have no pending verification. Please use the !verify command.")
                else:
                    try:
                        # Try to parse the message content as an integer
                        entered_code = int(message.content.strip())
                        if entered_code == correct_code:
                            # Code is correct
                            # Assign "Student" role to the user in the guild
                            guild = bot.get_guild(SERVER_ID)
                            member = guild.get_member(userID)
                            if member:
                                # Get the "Student" role
                                student_role = discord.utils.get(guild.roles, name='Student')
                                if student_role:
                                    try:
                                        await member.add_roles(student_role, reason="Verified")
                                        # Update the user's roles in the database
                                        cursor.execute(
                                            "UPDATE users SET roles = array_append(roles, %s), correct_code = NULL, attempts = 0 WHERE discord_id = %s",
                                            ('Student', userID)
                                        )
                                        conn.commit()
                                        await message.channel.send(
                                            "Verification successful! You have been assigned the 'Student' role."
                                        )
                                    except discord.Forbidden:
                                        await message.channel.send(
                                            "I do not have permission to assign roles in the server. Please contact an administrator."
                                        )
                                else:
                                    await message.channel.send(
                                        "The 'Student' role does not exist in the server. Please contact an administrator."
                                    )
                            else:
                                await message.channel.send("You are not a member of the server.")
                        else:
                            # Code is incorrect
                            attempts += 1
                            if attempts >= 5:
                                # Too many attempts
                                cursor.execute(
                                    "UPDATE users SET correct_code = NULL, attempts = %s WHERE discord_id = %s",
                                    (attempts, userID)
                                )
                                conn.commit()
                                await message.channel.send(
                                    "Too many incorrect attempts. Please request a new verification code using the !verify command."
                                )
                            else:
                                cursor.execute(
                                    "UPDATE users SET attempts = %s WHERE discord_id = %s",
                                    (attempts, userID)
                                )
                                conn.commit()
                                attempts_left = 5 - attempts
                                await message.channel.send(
                                    f"Incorrect code. You have {attempts_left} attempt(s) remaining."
                                )
                    except ValueError:
                        # Message content is not an integer
                        await message.channel.send("Please enter the verification code as a number.")
            else:
                # User is not awaiting verification
                await message.channel.send("You have no pending verification. Please use the !verify command.")
        except Exception as db_error:
            print(f"Database error: {db_error}")
            await message.channel.send("An error occurred while accessing the database.")
        finally:
            cursor.close()
            conn.close()
    else:
        # Process commands and other messages
        await bot.process_commands(message)
                
    