import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

/* loaded from: CodeRun.jar:com/gameobject/GiftManager.class */
public class GiftManager {
    private String fakeflag = "hacktoday{upsss_this_is_fake_flag_hehehe}";
    private String gift = "KHh19flIeUhU/3JYD7dnrIlkG2G9i7/YPHMpRgk1sim+MG3ZdwqTc44lvQVaojKH";
    long[] apaini = { 15125, 25570, 8745, 4148, 467, 4148, 15125, 467 };
    long apaan = 34393;
    long apeni = 3217;

    public boolean check(int x) {
        String v = Integer.toString(x);
        long[] data = new long[v.length()];
        for (int i = 0; i < v.length(); i++) {
            char c = v.charAt(i);
            // c = integer antara 0-9
            long value = (c + 7) * 99;
            // value = integer antara 693-1584
            long res = 1;
            long apeni2 = this.apeni;
            while (apeni2 > 0) {
                // Cek ganjil
                if ((apeni2 & 1) == 1) {
                    res = (res * value) % this.apaan;
                }
                apeni2 >>= 1;
                value = (value * value) % this.apaan;
            }
            data[i] = res;
        }
        int pjg = data.length;
        for (int i2 = 0; i2 < pjg; i2++) {
            int j = ((i2 * 9) + 9) % pjg;
            long temp = data[i2];
            data[i2] = data[j];
            data[j] = temp;
        }
        if (pjg != this.apaini.length) {
            return false;
        }
        for (int i3 = 0; i3 < pjg; i3++) {
            if (data[i3] != this.apaini[i3]) {
                return false;
            }
        }
        return true;
    }

    public String printgift(int x) {
        String key = Integer.toString(x);
        String rkey = new StringBuilder(key).reverse().toString();
        try {
            byte[] keyData = (String.valueOf(key) + rkey).getBytes("UTF-8");
            SecretKeySpec secretKeySpec = new SecretKeySpec(keyData, "AES");
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(2, secretKeySpec);
            byte[] decodedData = Base64.getDecoder().decode(this.gift);
            byte[] decrypted = cipher.doFinal(decodedData);
            return new String(decrypted, "UTF-8");
        } catch (Exception e) {
            e.printStackTrace();
            return this.fakeflag;
        }
    }

    public static void main(String[] args) {
        GiftManager giftManager = new GiftManager();
        if (args.length != 1) {
            System.out.println("Usage: java -jar CodeRun.jar <key>");
            return;
        }
        int key = Integer.parseInt(args[0]);
        if (giftManager.check(key)) {
            System.out.println(giftManager.printgift(key));
        } else {
            System.out.println(giftManager.fakeflag);
        }
    }
}