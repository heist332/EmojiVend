import discord
import sqlite3
import uuid
import datetime
import os.path
import asyncio
from datetime import timedelta
import random
import discord
import uuid
import sqlite3
import os
import asyncio
import random
import asyncio
import datetime
from datetime import timedelta

token = ""

client = discord.Client()


@client.event
async def on_ready():
    print(f"=====TOKEN=====\n{token}\n=====CLIENT ID=====\n{client.user.id}")


@client.event
async def on_message(message):
    if message.content.startswith("!생성 "):
        if int(message.author.id) == 839630971086831626:
            days = message.content.split(" ")[1]
            count = message.content.split(" ")[2]
            types = message.content.split(" ")[3]
            if days.isdigit():
                if count.isdigit():
                    if int(days) > 0 and int(count) > 0:
                        codelist = []
                        for codes in range(int(count)):
                            code = "EMOJI-" + str(uuid.uuid4()).upper()
                            codelist.append(code)
                            con = sqlite3.connect("license.db")
                            cur = con.cursor()
                            cur.execute(
                                "INSERT INTO licenses VALUES(?, ?, ?);", (code, days, types))
                            con.commit()
                        con.close()

                        keys = "\n".join(codelist)
                        await message.author.send(f"라이센스가 생성되었습니다.\n{keys}")
                    else:
                        await message.author.send("날짜, 개수는 0보다 커야합니다.")
                else:
                    await message.author.send("개수는 숫자로만 입력해주세요.")
            else:
                await message.author.send("날짜는 숫자로만 입력해주세요.")

    # ==============생성코드===================

    if message.content.startswith("!등록 "):
        if int(message.author.id) == 839630971086831626:
            await message.delete()
            code = message.content.split(" ")[1]
            if code.isdigit():
                await message.author.send("라이센스는 숫자로만 이루어져있지 않습니다.")
            else:
                con = sqlite3.connect("license.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM licenses WHERE key == ?;", (code,))
                key_info = cur.fetchone()
                con.close()
                if key_info == None:
                    await message.author.send("라이센스가 존재하지 않습니다.")
                    return
                else:
                    await message.author.send("잠시만 기다려주세요...")
                    con = sqlite3.connect("license.db")
                    cur = con.cursor()
                    cur.execute(
                        "DELETE FROM licenses WHERE key == ?;", (code,))
                    con.commit()
                    con.close()
                    pw = "ADMIN-" + str(message.guild.id)
                    await message.author.send(f"라이센스 등록이 완료되었습니다.\n[ 등록 성공한 코드 ] : {code}\n[ 기한 ] : {key_info[1]}\n[ 타입 ] : {key_info[2]}\n[ 비밀번호 ] : {pw}")
                    con = sqlite3.connect(
                        f"database/{str(message.guild.id)}.db")
                    cur = con.cursor()

                    cur.execute(
                        "CREATE TABLE configs (expiringdate TEXT, pw TEXT, emojimsg INTEGER, cid TEXT, cpw TEXT);")
                    con.commit()
                    cur.execute(
                        "CREATE TABLE products (id TEXT, name TEXT, price INTEGER, stocks TEXT);")
                    con.commit()
                    cur.execute(
                        "CREATE TABLE users (id INTEGER, balance INTEGER);")
                    con.commit()
                    cur.execute("INSERT INTO configs VALUES(?, ?, ?, ?, ?);",
                                (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), pw, 0, "", ""))
                con.commit()
                con.close()

    if message.content == "!이모지":
        if int(message.author.id) == 839630971086831626:
            await message.delete()
            try:
                file = f"C:/Users/Heist/Desktop/Project/emojivend/database/{str(message.guild.id)}.db"
                if os.path.isfile(file):

                    emoji = await message.channel.send("아래 이모지를 눌러 자판기를 이용하세요.")
                    reaction = await emoji.add_reaction("🔗")
                    con = sqlite3.connect(
                        f"database/{str(message.guild.id)}.db")
                    cur = con.cursor()
                    cur.execute("UPDATE configs SET emojimsg = ?;",
                                (emoji.id,))
                    con.commit()
                    con.close()
                else:
                    await message.author.send("라이센스가 등록되지 않은 서버입니다.")
            except Exception as e:
                if str(e) == "'NoneType' object has no attribute 'id'":
                    await message.author.send("라이센스가 등록되지 않은 서버입니다.")
                else:
                    print(e)

    if message.content.startswith("!연장 "):
        if int(message.author.id) == 839630971086831626:
            try:
                file = f"C:/Users/Heist/Desktop/Project/emojivend/database/{str(message.guild.id)}.db"
                if os.path.isfile(file):
                    # ============================
                    try:
                        id = message.guild.id
                        license = message.content.split(" ")[1]
                        con = sqlite3.connect(
                            f"database/{str(message.guild.id)}.db")
                        cur = con.cursor()
                        cur.execute(
                            "SELECT * FROM keys WHERE key == ?;", (license,))
                        key_info = cur.fetchone()
                        if key_info == None:
                            con.close()
                            await message.author.send("존재하지 않는 코드입니다.")
                            return
                        cur.execute(
                            "DELETE FROM keys WHERE key == ?;", (license,))
                        con.commit()
                        con.close()
                        con = sqlite3.connect(
                            f"database/{str(message.guild.id)}.db")
                        cur = con.cursor()
                        cur.execute(
                            "SELECT * FROM configs;")
                        guild_info = cur.fetchone()
                        if (guild_info == None):
                            con.close()
                            await message.author.send("연장할 서버를 찾지 못했습니다.")
                            return
                        con.close()

                        new_license_remaining = (datetime.datetime.strptime(
                            guild_info[0], '%Y-%m-%d %H:%M') + timedelta(days=key_info[1])).strftime('%Y-%m-%d %H:%M')
                        con = sqlite3.connect(
                            f"database/{str(message.guild.id)}.db")
                        cur = con.cursor()
                        cur.execute("UPDATE configs SET expiringdate = ?;",
                                    (new_license_remaining,))
                        con.commit()
                        con.close()
                        await message.author.send(embed=discord.Embed(title=":white_check_mark: **라이센스 연장 성공**", description=f"**{id}서버의 라이센스 연장을 성공했습니다.**"))
                    except Exception as e:
                        print(e)
                        await message.author.send("연장에 실패했습니다.")
                        return
                else:
                    await message.author.send("라이센스가 등록되지 않은 서버입니다.")
            except Exception as e:
                if str(e) == "'NoneType' object has no attribute 'id'":
                    await message.author.send("라이센스가 등록되지 않은 서버입니다.")


@client.event
async def on_raw_reaction_add(reaction):

    try:
        file = f"C:/Users/Heist/Desktop/Project/emojivend/database/{str(reaction.member.guild.id)}.db"
        if os.path.isfile(file):
            con = sqlite3.connect(
                f"database/{str(reaction.member.guild.id)}.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;",
                        (reaction.user_id,))
            user_info = cur.fetchone()
            con.close()
            if user_info == None:
                con = sqlite3.connect(
                    f"database/{str(reaction.member.guild.id)}.db")
                cur = con.cursor()
                cur.execute("INSERT INTO users VALUES(?, ?);",
                            (reaction.user_id, 0,))
                con.commit()
                con.close()

            if reaction.member.bot == False:
                con = sqlite3.connect(
                    f"database/{str(reaction.member.guild.id)}.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM configs;")
                configs = cur.fetchone()
                con.close()

                if reaction.message_id == configs[2]:
                    if reaction.emoji.name == "🔗":
                        channel = await client.fetch_channel(reaction.channel_id)
                        message = await channel.fetch_message(reaction.message_id)
                        await message.clear_reaction("🔗")
                        await message.add_reaction("🔗")
                        msg = await reaction.member.send("아래 항목에서 원하는 번호 이미지를 눌러주세요.\n:zero: : 제품목록\n:one: : 정보\n:two: : 충전\n:three: : 구매")
                        await msg.add_reaction("0️⃣")
                        await msg.add_reaction("1️⃣")
                        await msg.add_reaction("2️⃣")
                        await msg.add_reaction("3️⃣")

                        def check(reactions):
                            return (reactions.user_id != client.user.id)

                        try:
                            reactions = await client.wait_for('raw_reaction_add', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            try:
                                await reaction.member.send("제한시간이 다 되었습니다.")
                            except:
                                pass
                            return None

                        if reactions.emoji.name == "0️⃣":
                            await msg.delete()
                            con = sqlite3.connect(
                                f"database/{str(reaction.member.guild.id)}.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM products;")
                            products = cur.fetchall()
                            con.close()
                            products_embed = discord.Embed(
                                title="제품목록", description="제품목록입니다.")
                            br = "\n"
                            for product in products:
                                products_embed.add_field(
                                    inline=True, name=f"`{product[1]}`", value=f"`{str(product[2])}`원  {br}재고 `{str(len(product[3].split(br))) if product[3] != '' else '0'}`개")
                            await reaction.member.send(embed=products_embed)

                        if reactions.emoji.name == "1️⃣":
                            await msg.delete()
                            con = sqlite3.connect(
                                f"database/{str(reaction.member.guild.id)}.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;",
                                        (reactions.user_id,))
                            user_info = cur.fetchone()
                            print(user_info)
                            con.close()
                            if user_info == None:
                                await reaction.member.send("가입이 안된 유저입니다.")
                                return
                            status = discord.Embed(
                                title="정보조회", description=f"닉네임: {reaction.member.name}\n아이디: {reaction.user_id}\n잔액: {user_info[1]}원")
                            await reaction.member.send(embed=status)

                        if reactions.emoji.name == "2️⃣":
                            # 문상충전부분
                            await reaction.member.send("충전 대기중입니다.")

                        if reactions.emoji.name == "3️⃣":
                            await msg.delete()
                            con = sqlite3.connect(
                                f"database/{str(reaction.member.guild.id)}.db")
                            cur = con.cursor()
                            cur.execute(
                                "SELECT * FROM users WHERE id == ?;", (reaction.user_id,))
                            user_info = cur.fetchone()
                            cur.execute("SELECT * FROM products;")
                            products = cur.fetchall()
                            con.close()
                            if user_info == None:
                                await reaction.member.send("가입되지 않았습니다.")
                                return

                            options = discord.Embed(
                                title="제품 목록", description="제품목록입니다.")
                            br = "\n"

                            names = []

                            i = 0
                            for product in products:
                                i = int(i) + 1
                                options.add_field(
                                    inline=True, name=f"`{product[1]}`", value=f"번호 {i}번\n`{str(product[2])}`원  {br}재고 `{str(len(product[3].split(br))) if product[3] != '' else '0'}`개")
                                names.append(product[1])

                            print(names)

                            msgs = await reaction.member.send(embed=options)

                            try:

                                msges = await client.wait_for("message", timeout=60, check=lambda m: isinstance(m.channel, discord.channel.DMChannel) and (m.author.id == reaction.user_id))
                                if not msges.content.isdigit():
                                    await reaction.member.send("번호는 숫자로만 입력해주세요.")
                                    return
                                if int(msges.content) > i or int(msges.content) < 0:
                                    await reaction.member.send("번호가 알맞지 않습니다.")
                                    return
                            except asyncio.TimeoutError:
                                try:
                                    await msgs.delete()
                                except:
                                    pass
                                return

                            try:
                                await msgs.delete()
                            except Exception as e:
                                print(e)
                                pass
                            try:

                                await reaction.member.send(f"잠시만 기다려주세요.\n입력하신 번호 : {msges.content}")
                                con = sqlite3.connect(
                                    f"database/{str(reaction.member.guild.id)}.db")
                                cur = con.cursor()
                                cur.execute(
                                    "SELECT * FROM products WHERE name == ?;", (names[int(msges.content) - 1]))
                                products_info = cur.fetchone()
                                con.close()
                                print(products_info[0])
                                con = sqlite3.connect(
                                    f"database/{str(reaction.member.guild.id)}.db")
                                cur = con.cursor()
                                cur.execute(
                                    "SELECT * FROM users WHERE id == ?;", (reaction.user_id,))
                                user_info = cur.fetchone()
                                cur.execute(
                                    "SELECT * FROM products WHERE id == ?;", (products_info[0],))
                                product_info = cur.fetchone()

                                if product_info == None:
                                    con.close()
                                    try:
                                        await reaction.member.send("오류가 발생했습니다.")
                                    except:
                                        pass
                                    return

                                if product_info[2] > user_info[1]:
                                    con.close()
                                    try:
                                        await reaction.member.send("잔액이 부족합니다.")
                                    except:
                                        pass
                                    return

                                if (len(product_info[3].split("\n")) if product_info[3] != "" else 0) == 0:
                                    con.close()
                                    try:
                                        await reaction.member.send("재고가 부족합니다.")
                                    except:
                                        pass
                                    return

                                try:
                                    await msgs.delete()
                                except:
                                    pass

                                con = sqlite3.connect(
                                    f"database/{str(reaction.member.guild.id)}.db")
                                cur = con.cursor()
                                cur.execute(
                                    "SELECT * FROM users WHERE id == ?;", (reaction.user_id,))
                                user_info = cur.fetchone()
                                cur.execute(
                                    "SELECT * FROM products WHERE id == ?;", (products_info[0],))
                                product_info = cur.fetchone()

                                if product_info[2] > user_info[1]:
                                    try:
                                        await msgs.delete()
                                    except:
                                        pass
                                    con.close()
                                    try:
                                        await reaction.member.send("잔액이 부족합니다.")
                                    except:
                                        pass
                                    return

                                if (len(product_info[3].split("\n")) if product_info[3] != "" else 0) < 1:
                                    try:
                                        await msgs.delete()
                                    except:
                                        pass
                                    con.close()
                                    try:
                                        await reaction.member.send("재고가 부족합니다.")
                                    except:
                                        pass
                                    return

                                cur.execute(
                                    "UPDATE users SET balance = balance - ? WHERE id == ?;", (product_info[2], reaction.user_id))
                                con.commit()
                                cur_stock = product_info[3].split("\n")
                                stock_sold = random.choice(cur_stock)
                                cur_stock.remove(stock_sold)
                                cur.execute("UPDATE products SET stocks = ? WHERE id == ?;", ("\n".join(
                                    cur_stock), products_info[0]))
                                con.commit()
                                con.close()

                                try:
                                    await reaction.member.send(embed=discord.Embed(title="구매해주셔서 감사합니다!", description=f"제품 가격: {str(product_info[2])}원\n구매 후 잔액: {str(user_info[1] - product_info[2])}원"))
                                    await reaction.member.send(stock_sold)
                                except:
                                    pass
                            except Exception as e:
                                print(str(e))
                else:
                    print("돌아가라")
                    return
            else:
                return
            # if user.bot == False:
            #     print(reaction)
            #     if reaction == "🔗"
        else:
            return
    except Exception as e:
        if str(e) == "'NoneType' object has no attribute 'id'" or str(e) == "'NoneType' object has no attribute 'guild'":
            return


client.run(token)
